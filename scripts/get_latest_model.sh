#!/usr/bin/env bash

set -e

BUCKET="s3://fwhigh-predictive-models"
MODEL_ID=$(aws s3 ls ${BUCKET}/models/ | awk '$1~/PRE/ {print $2}' | sed 's/\///g' | sort -nr | head -n 1)
S3_DIR=$BUCKET/models/$MODEL_ID
DIR=data

echo Getting data from $S3_DIR
echo Writing it to $DIR

mkdir -p $DIR

aws s3 cp --recursive --exclude "*" --include "model.pkl" $S3_DIR/ $DIR/