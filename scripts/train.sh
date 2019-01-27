#!/usr/bin/env bash

set -e

MODEL_ID=`date +%Y%m%d`
S3_DIR=$BUCKET/models/$MODEL_ID
DIR=data

echo MODEL_ID $MODEL_ID
echo S3_DIR $S3_DIR
echo DIR $DIR

TRAINING_ID=$(aws s3 ls $BUCKET/training/ | awk '$1~/PRE/ {print $2}' | sed 's/\///g' | sort -nr | head -n 1)

echo $TRAINING_ID TRAINING_ID

mkdir -p $DIR

# Get the data. Replace this line with something like:
#   aws s3 cp $BUCKET/training-data/ $DIR/
# to train on new data that's placed into S3 directly.
bash scripts/get_training_data.sh $BUCKET/training/$TRAINING_ID $DIR

# Train the model
papermill notebooks/model-training.ipynb $DIR/model-training-$MODEL_ID.ipynb -p DATA_DIR $DIR

# Convert the notebook into HTML
jupyter nbconvert --to html $DIR/model-training-$MODEL_ID.ipynb

# Push any assets to the cloud
if [ "$ENVIRONMENT" == "staging" ]; then
    echo Pushing model to S3
    aws s3 cp $DIR/ $S3_DIR/ \
         --recursive --exclude "*" --include "*.ipynb" --include "*.html" --include "*.pkl"
fi
