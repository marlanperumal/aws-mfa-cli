from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aws-mfa-cli",
    version="0.0.5",
    author="Marlan Perumal",
    author_email="marlan.perumal@gmail.com",
    description="CLI tool for managing AWS MFA credentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marlanperumal/aws-mfa-cli",
    py_modules=["aws_mfa"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        aws-mfa=aws_mfa:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)