# pmip

Predictive Models in Production

## Workflow

This is the regular workflow once you've got the whole system set up.

1. Edit code and commit to Github.
1. Build the Docker image locally.
1. Push the Docker image to the AWS ECR repository (command below).
1. Manually upload the latest model to AWS S3 s3://<your-S3-bucket>/models/staging/YYYYMMDD/, where YYYYMMDD is today.
1. Deploy the AWS ElasticBeanstalk API with `eb deploy`. This should pick up the S3 model you just uploaded.
1. Run the AWS Batch training job. This will make a new model (again) and restart the EB application (again).

## Local dev

### Pro tips

If you ever find yourself with a "no space left on device" error when building the Docker image, try

```bash
docker rm $(docker ps -q -f 'status=exited')
docker rmi $(docker images -q -f "dangling=true")
```

I recommend setting `BUCKET` in `~/.profile`.

```bash
export BUCKET=<your-S3-bucket>
```

### Build the base training image

```bash
bash scripts/build_training_image.sh
```

### Do interactive model training and data exploration in the Jupyter notebook

```bash
ENVIRONMENT=dev bash scripts/run_training_container.sh -c "jupyter notebook notebooks/ --allow-root --ip=0.0.0.0 --port=8888 --no-browser"
```

Then open [http://localhost:8888](http://localhost:8888) to run Jupyter.

If you need to enter into the container's shell, do this.

```bash
ENVIRONMENT=dev BUCKET=$BUCKET bash scripts/run_training_container.sh -
```

### Train a model programmatically

```bash
ENVIRONMENT=dev BUCKET=$BUCKET bash scripts/run_training_container.sh scripts/train.sh
```

### Pushing the new Docker image to production for the training and Flask API services

If this is your first or only ECR repo, then run

```bash
bash scripts/push_training_image.sh $(aws ecr describe-repositories | jq -r '.repositories[0].repositoryUri')
```

You have have multiple ECR repos you'll have to change the argument so that it points to the one you want to push to. 

#### Build the Flask API image

```bash
bash scripts/build_api_image.sh
```

#### Run the Flask API locally 

Run the Flask API locally outside of the Docker container.

```bash
ENVIRONMENT=dev bash scripts/run_api_container.sh "python -m pmip.routes"
```

Then open [http://localhost:8000](http://localhost:8000) to view the Swagger documentation and issue API calls.

Run the Flask API locally inside your Docker container.

```bash
ENVIRONMENT=dev BUCKET=$BUCKET bash scripts/run_api_container.sh
```

Then open [http://localhost:8000](http://localhost:8000) to view the Swagger documentation and issue API calls.

Drop into the Flask API container.

```bash
ENVIRONMENT=dev bash scripts/run_api_container.sh -
```

### Deploy the ElasticBeanstalk 

If this is the first time, run

```bash
eb init
```

To deploy run

```bash
eb deploy
```

### Push the Lambda API to Lambda

```bash
BUCKET=$BUCKET serverless deploy --region $([ -z "$AWS_DEFAULT_REGION" ] && aws configure get region || echo "$AWS_DEFAULT_REGION")
``` 

Issue API calls.

```bash
curl -X GET https://lrgbpftjy3.execute-api.us-west-1.amazonaws.com/dev/healthcheck
curl -X GET https://lrgbpftjy3.execute-api.us-west-1.amazonaws.com/dev/model-info
curl -X POST -d '{"comments":["Check out this free stuff","I take issue with your characterization"]}' \
    https://lrgbpftjy3.execute-api.us-west-1.amazonaws.com/dev/predict?flavor=class
```

## Resources

* https://github.com/pypa/sampleproject/blob/master/setup.py
