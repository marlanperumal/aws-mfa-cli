# AWS MFA CLI

Command Line tool for managing AWS MFA credentials.

## Quickstart

Install with

```bash
python3 -m pip install aws-mfa-cli
```

Setup MFA device

```bash
aws-mfa device set <mfa-device-arn>
```

Enable Profile to use MFA

```bash
aws-mfa profile enable <profile-name>
```

Authenticate with MFA token

```bash
aws-mfa token <mfa-token>
```

Test it works

```bash
aws s3 ls --profile <profile-name>
```