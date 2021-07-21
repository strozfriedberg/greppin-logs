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

from pathlib import Path

from aws_cdk import (
    aws_iam as iam,
    aws_lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notify,
    core as cdk,
)


class LogsStack(cdk.Stack):
    """Logs S3 bucket and lambda to process logs."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        bucket_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket with public access blocked by default and versioning enabled
        self.bucket = s3.Bucket(
            self,
            "LogsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            bucket_name=bucket_name,
            versioned=True,
        )
        
        code_path = (Path(__file__)
            .parents[2]
            .joinpath('lambda-functions', 'process-logs', 'process_logs').resolve())
        # Create lambda function from proceess_logs.lambda_function.lambda_handler
        # using Python 3.8 runtime and passing the bucket name as an environment variable
        self.lambda_function = aws_lambda.Function(
            self,
            "LambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            environment={
                "BUCKET_NAME": self.bucket.bucket_name,
            },
            code=aws_lambda.Code.from_asset(
                f"{code_path}",
                # Exclude non-code files
                exclude=[".venv", "poetry.lock", "pyproject.toml"],
            ),
        )
        # Grant the lambda function execution role read access to the bucket
        self.bucket.grant_read(self.lambda_function)
        
        # Trigger the lambda every time an object is uploaded to the bucket
        self.notification = s3_notify.LambdaDestination(self.lambda_function)
        self.notification.bind(self, self.bucket)
        self.bucket.add_object_created_notification(self.notification)
