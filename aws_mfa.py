from subprocess import run, PIPE, STDOUT
import os
import json

import click

MFA_PROFILE = os.environ.get("AWS_MFA_PROFILE", "mfa-profile")


def get_config(key, profile):
    result = run(["aws", "configure", "--profile", profile, "get", key], stdout=PIPE, stderr=STDOUT)
    if result.returncode != 0:
        click.echo(result.stdout)
        raise click.Abort()
    return result.stdout.decode("UTF-8").strip()


def set_config(key, value, profile):
    result = run(["aws", "configure", "--profile", profile, "set", key, value])
    if result.returncode != 0:
        click.echo(result.stdout)
        raise click.Abort()
    return result.returncode


def get_session_token(mfa_device, token):
    result = run([
            "aws", "sts", "get-session-token",
            "--serial-number", mfa_device, "--token-code", token
        ],
        stdout=PIPE, stderr=STDOUT
    )
    if result.returncode != 0:
        click.echo(result.stdout)
        raise click.Abort()
    credentials = json.loads(result.stdout)["Credentials"]
    return {
        "access_key_id": credentials["AccessKeyId"],
        "secret_access_key": credentials["SecretAccessKey"],
        "session_token": credentials["SessionToken"],
        "expiration": credentials["Expiration"],
    }


def set_mfa_credentials(access_key_id, secret_access_key, session_token):
    set_config("aws_access_key_id", access_key_id, MFA_PROFILE)
    set_config("aws_secret_access_key", secret_access_key, MFA_PROFILE)
    set_config("aws_session_token", session_token, MFA_PROFILE)


def clear_env_mfa_credentials():
    if os.environ.get("AWS_ACCESS_KEY_ID"):
        del os.environ["AWS_ACCESS_KEY_ID"]
    if os.environ.get("AWS_SECRET_ACCESS_KEY"):
        del os.environ["AWS_SECRET_ACCESS_KEY"]
    if os.environ.get("AWS_SESSION_TOKEN"):
        del os.environ["AWS_SESSION_TOKEN"]


def set_env_mfa_credentials(access_key_id, secret_access_key, session_token):
    print(f"# Run the export statements below")
    print(f"# Or re-execute this command with `eval $(command)`")
    print(f"export AWS_ACCESS_KEY_ID={access_key_id}")
    print(f"export AWS_SECRET_ACCESS_KEY={secret_access_key}")
    print(f"export AWS_SESSION_TOKEN={session_token}")


@click.group()
def cli():
    clear_env_mfa_credentials()


@click.group()
def profile():
    pass


@click.group()
def device():
    pass


@click.command()
@click.option(
    "--device",
    default=None,
    help="AWS ARN for the MFA device used to obtain the token"
)
@click.argument("code")
def token(code, device):
    if device is None:
        device = get_config("aws_mfa_device", MFA_PROFILE)
    click.echo(f"Logging in with token code {code} from MFA device {device}")
    credentials = get_session_token(device, code)
    click.echo()
    click.echo(credentials)
    click.echo()
    set_mfa_credentials(
        credentials["access_key_id"],
        credentials["secret_access_key"],
        credentials["session_token"],
    )
    expiration = credentials["expiration"]
    click.echo(f"Token expires at {expiration}")


@click.command("set")
@click.argument("arn")
def set_device(arn):
    set_config("aws_mfa_device", arn, MFA_PROFILE)


@click.command("get")
def get_device():
    arn = get_config("aws_mfa_device", MFA_PROFILE)
    click.echo(arn)


@click.command("enable")
@click.argument("profiles", nargs=-1)
def enable_profile(profiles):
    for profile in profiles:
        set_config("source_profile", MFA_PROFILE, profile)


@click.command("disable")
@click.argument("profiles", nargs=-1)
def disable_profile(profiles):
    for profile in profiles:
        set_config("source_profile", "default", profile)


cli.add_command(token)
cli.add_command(device)
cli.add_command(profile)
device.add_command(get_device)
device.add_command(set_device)
profile.add_command(enable_profile)
profile.add_command(disable_profile)


if __name__ == "__main__":
    cli()