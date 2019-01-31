#!/usr/bin/env bash

# Push any assets to the cloud
if [ ! -f "data/model.pkl" ]; then
    bash scripts/get_latest_model.sh
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
    docker run -it -p 8000:8000 \
        --mount type=bind,source="$(pwd)",target=/usr/src/app \
        -e AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id) \
        -e AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key) \
        -e AWS_DEFAULT_REGION=$(aws configure get region) \
        -e BUCKET=$BUCKET \
        -e ENVIRONMENT=$ENVIRONMENT \
        -t pmip_api:latest
else
    docker run -it -p 8000:8000 \
        --mount type=bind,source="$(pwd)",target=/usr/src/app \
        -e AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id) \
        -e AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key) \
        -e AWS_DEFAULT_REGION=$(aws configure get region) \
        -e BUCKET=$BUCKET \
        -e ENVIRONMENT=$ENVIRONMENT \
        -t pmip_api:latest "$@"
fi
