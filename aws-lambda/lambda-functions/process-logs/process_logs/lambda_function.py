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

import boto3


def lambda_handler(event, context) -> int:
    """Print the bucket name and key of objects uploaded to an S3 bucket.
    """
    if not "BUCKET_NAME" in ENV:
        print("::: ERROR: Must provide BUCKET_NAME env variable")
        return 1

    if len(event["Records"]) == 0:
        print("::: ERROR: No events found, expected one")
        return 1
    if len(event["Records"]) > 1:
        print("::: WARNING: More than one event found, processing the first and skipping the rest")

    bucket_name = ENV["BUCKET_NAME"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    print(f"::: INFO: Object {object_key} upload to bucket {bucket_name}")
    
    ## Process new S3 object

    return 0
