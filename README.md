# pmip

Predictive Models in Production

## Local dev

### Pro tips

If you ever find yourself with a "no space left on device" error when building the Docker image, try

```bash
docker rm $(docker ps -q -f 'status=exited')
docker rmi $(docker images -q -f "dangling=true")
```

### Build the base training image

```bash
ENVIRONMENT=dev bash scripts/build_training_image.sh
```

### Do interactive model training and data exploration in the Jupyter notebook

```bash
ENVIRONMENT=dev bash scripts/run_training_container.sh -c jupyter notebook notebooks/ --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```

Then open [http://localhost:8888](http://localhost:8888) to run Jupyter.

### Train a model programmatically

```bash
ENVIRONMENT=dev bash scripts/run_training_container.sh scripts/train.sh
```

### Pushing the new Docker image to production for the training and API services

If this is your first and only ECR repo, then run

```bash
bash scripts/push_image.sh $(aws ecr describe-repositories | jq -r '.repositories[0].repositoryUri')
```

You have have multiple ECR repos you'll have to change the argument so that it points to the one you want to push to. 

## Resources

* https://github.com/pypa/sampleproject/blob/master/setup.py