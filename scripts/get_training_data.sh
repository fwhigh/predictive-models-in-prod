#!/usr/bin/env bash

S3_DIR=$1
DIR=$2

echo Getting data from $S3_DIR
echo Writing it to $DIR

aws s3 cp --recursive $S3_DIR/ $DIR/
cd $DIR
unzip *.zip
