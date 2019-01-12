#!/usr/bin/env bash

ECR_URI=$1
AWS_REGION=$(aws configure get region)

IMAGE_TAG=latest

$(aws ecr get-login --no-include-email --region $AWS_REGION)
docker tag pmip:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
docker push ${ECR_URI}:${IMAGE_TAG}
