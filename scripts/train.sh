#!/usr/bin/env bash

set -e

RUNID=`date +%Y%m%d`
DATA_DIR=data/${RUNID}
BUCKET="s3://predictive-models"
S3_DATA_DIR=${BUCKET}/${RUNID}

mkdir -p DATA_DIR

# Get the data. Replace this line with something like:
#   aws s3 cp $BUCKET/training-data/ $DATA_DIR/
# to train on new data that's placed into S3 directly.
bash scripts/get_training_data.sh ${DATA_DIR}

# Train the model
papermill notebooks/model-training.ipynb ${DATA_DIR}/model-training-${RUNID}.ipynb \
    -p RUNID ${RUNID} -p DATA_DIR ${DATA_DIR}

# Convert the notebook into HTML
jupyter nbconvert --to html ${DATA_DIR}/model-training-${RUNID}.ipynb

# Push any assets to the cloud
if [ "$ENVIRONMENT" == "staging" ]; then
    aws s3 cp --exclude * --include *.ipynb *.html *.pkl ${DATA_DIR}/ S3_DATA_DIR/
fi