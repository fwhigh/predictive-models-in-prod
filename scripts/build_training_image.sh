#!/usr/bin/env bash

docker build \
    --build-arg AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) \
    --build-arg AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) \
    --build-arg AWS_DEFAULT_REGION=$(aws configure get region) \
    --build-arg GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN \
    --build-arg ENVIRONMENT=$ENVIRONMENT \
    -f Dockerfile.train -t pmip:latest .
