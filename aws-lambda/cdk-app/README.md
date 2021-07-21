# Processing Logs with Lambdas: Template CDK App

## Overview

This [AWS CDK](https://aws.amazon.com/cdk/) app is a template (starter app)
for deploying lambda functions to process objects uploaded to [S3 buckets](https://aws.amazon.com/s3/).
It comes with code to create an S3 bucket, a lambda function with permissions to read objects from the bucket,
and a trigger to run the lambda when a new object is uploaded to the bucket.
This setup is useful when you know the kind of processing required on a set of logs beforehand,
and want to parse new data as it's uploaded to the bucket.

## Getting Started

### Installing Dependencies

The [AWS CDK documentation](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_prerequisites)
is a great place to go for in-depth documentation on working with the CDK.
To get started quickly, make sure you have the following installed (or in a Docker container):

1. [NodeJS](https://nodejs.org/en/) v10.13.0 or later
2. [npm](https://www.npmjs.com/) (should be installed with NodeJS)
3. [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_install)
4. [Python 3.6](https://www.python.org/downloads/) or later
5. [Pip for Python3](https://pypi.org/project/pip/) (should be installed with Python)
6. [venv module for Python3](https://docs.python.org/3/library/venv.html) or [Poetry](https://python-poetry.org/docs/)

If installing the AWS CDK via `npm install -g` gives you permissions trouble,
you can install it locally in a directory with `npm install` then the CDK entrypoint to your `PATH`.

```bash
mkdir /some/directory/aws-cdk && cd /some/directory/aws-cdk
npm install aws-cdk # install CDK locally in the directory
export PATH=/some/directory/aws-cdk/node_modules/.bin:$PATH # put this in .bashrc or .bash_profile
```

If you want to update the CDK when new versions are released, you can do that with the following:

```bash
cd /some/directory/aws-cdk
npm up aws-cdk
```

### Installing the CDK app package

Once you have all the dependencies installed, cd to the [cdk-app](aws-lambda/cdk-app) directory and run:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip wheel
pip install -e .
```

### Editing the Lambda Function

At this point you will have installed the all the necessary dependencies and created a Python virtual environment
to use for deployment. The lambda handler in [lambda\_function.py](../lambda-functions/process-logs/process_logs/lambda_function.py)
just runs some basic checks and prints the name of each object uploaded. You should add code to do something meaningful,
such as parse records from CloudTrail logs and grep for events (after all, we are here to grep some logs):

```python
import json

# snip

def lambda_handler(event, context) -> int:
    # snip

    client = boto3.client("s3")
    response = client.get_object(
        Bucket=bucket_name,
        Key=object_key,
    )
    object_content = response["Body"].read()
    cloudtrail_records = json.loads(object_content)

    for record in cloudtrail_records["Records"]:
        if record["eventName"] in {"GetObject", "PutObject", "DeleteObject", "StartInstance"}:
            # Extract fields from record and do something with them
```

### Deployment

The CDK app requires a small [TOML](https://toml.io/en/) config file with the following fields:

```toml
# config.toml
account = "<AWS account ID>"
region = "<AWS region for deployment>"
bucket_name = "<S3 bucket name>"
```

This tells the CDK where to deploy the stack and what name to assign to the S3 bucket.
To deploy the stack run the following command _within the Python virtual environment_:

```bash
CDK_CONFIG_FILE=<config_name>.toml cdk deploy greppin-logs
```

## References

1. AWS CDK Python reference: https://docs.aws.amazon.com/cdk/api/latest/python/index.html
2. S3 Bucket construct: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
3. S3 Notifications for Lambdas: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3_notifications/LambdaDestination.html
4. Lambda Function construct: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html
5. Lambda Code construct: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Code.html
6. AWS Lambda-S3 example: https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
