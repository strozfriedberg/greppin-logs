#!/usr/bin/env python3
## Copyright 2021 Stroz Friedberg, LLC, An Aon Company
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from os import environ as ENV
from pathlib import Path
import typing

from aws_cdk import core as cdk
import toml

from cdk_app.logs_stack import LogsStack


_REQUIRED_CONFIG_OPTIONS = (
    "account",
    "region",
    "bucket_name",
)
_STATIC_TAGS = {
    # "Name": "Value",
}


def gen_and_validate_config() -> typing.Dict[str, typing.Any]:
    """Read the config file as TOML and
    validate the options against ``_REQUIRED_CONFIG_OPTIONS``.
    """
    if "CDK_CONFIG_FILE" not in ENV:
        raise ValueError("Must set CDK_CONFIG_FILE env variable")
    config_file_path = Path(ENV["CDK_CONFIG_FILE"])
    if not config_file_path.is_file():
        raise FileNotFoundError(f"Config file {config_file_path} either is not a file or does not exist")

    config = toml.load(config_file_path)
    for option in _REQUIRED_CONFIG_OPTIONS:
        if option not in config:
            raise ValueError(f"Must provide '{option}' in config")
    return config


def main() -> int:
    # Read and validate the config file pointed to by CDK_CONFIG_FILE env variable
    config = gen_and_validate_config()
    # Create a CDK "environment" so CDK knows where to deploy the stack
    env = cdk.Environment(account=config["account"], region=config["region"])
    # Initialize the app
    app = cdk.App()

    # Initialize the log processing stack with the bucket name from config file
    logs_stack = LogsStack(
        app,
        "greppin-logs",
        config["bucket_name"],
        description="Greppin' Logs AWS template stack",
        env=env,
    )
    # Apply tags to all resources created within the logs_stack
    for key, value in _STATIC_TAGS.items():
        cdk.Tags.of(logs_stack).add(key, value)

    app.synth()
    return 0


if __name__ == "__main__":
    main()
