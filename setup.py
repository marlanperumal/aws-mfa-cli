from setuptools import setup

setup(
    name="aws-mfa-cli",
    version="0.0.1",
    py_modules=["aws_mfa"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        aws-mfa=aws-mfa.cli
    """
)