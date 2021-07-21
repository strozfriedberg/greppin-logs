# Greppin' Logs: Leveling Up Log Analysis

## Overview

This repo contains sample code and example datasets from Jon Stewart and Noah Rubin's presentation at the
[2021 SANS DFIR Summit](https://www.sans.org/cyber-security-training-events/digital-forensics-summit-2021/#agenda) titled Greppin' Logs.
The talk was centered around the idea that Forensics is Data Engineering and Data Science, and should be approached as such.
Jon and Noah focused on the core (Unix) command line tools useful to anyone analyzing datasets from a terminal,
purpose-built tools for handling structured tabular and JSON data, Stroz Friedberg's open source multipattern search tool
[Lightgrep](https://github.com/strozfriedberg/lightgrep), and scaling with AWS.

## Repository Contents

### Command Line Examples

The [command-line](command-line/) directory contains shell scripts (`.sh` files) with the commands from each CLI tool example from the presentation,
as well as a [Dockerfile](command-line/Dockerfile) containing the tools used in the presentation.
To build the Docker image with the tag `greppin-logs:latest`, make sure [Docker is installed](https://docs.docker.com/engine/install/)
and run the following command from the root of the repo:

```bash
docker build -f command-line/Dockerfile -t greppin-logs:latest .
```

We've also included in the Docker image a Python virtual environment containing the foundational Python data science libraries (numpy, scipy, pandas, etc.),
an installation of R and the Tidyverse packages, as well as the command line plotting tool Rush.
Links to the documentation for each tool are present in comments in the Dockerfile.
To run the Docker container and test out the tools with the sample datasets, run the following in root of the repo after building the image above:

```bash
docker run --rm --name greppin-logs-playground -v "$(pwd)/datasets":/workspaces/examples/datasets/ -it --entrypoint bash greppin-logs:latest
```

### Datasets

The [datasets](datasets/) directory contains some of the example datasets used in the presentation:

1. [employees.csv](datasets/employees.csv): Fake employees names, email addresses, and employment status keyed by `id`.
2. [salaries.csv](datasets/salaries.csv): Fake employee salaries keyed by `id`.
3. [cloudtrail-log.gz](datasets/cloudtrail-log.gz): [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) sample log record.

### Template AWS CDK App

The [aws-lambda](aws-lambda/) directory contains a template [AWS CDK](https://aws.amazon.com/cdk/) app and lambda function for processing files uploaded to an S3 bucket.
See the [README](aws-lambda/cdk-app/README.md) in that directory for more information on how to modify the Lambda code and deploy the stack to AWS.
