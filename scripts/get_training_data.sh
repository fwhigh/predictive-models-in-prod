#!/usr/bin/env bash

set -e

$DIR=$1

cd $DIR
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00380/YouTube-Spam-Collection-v1.zip
unzip YouTube-Spam-Collection-v1.zip
