# pmip

Predictive Models in Production

## Local dev

If you ever find yourself with a "no space left on device" error, try

```bash
docker rm $(docker ps -q -f 'status=exited')
docker rmi $(docker images -q -f "dangling=true")
```

See, eg, https://forums.docker.com/t/no-space-left-on-device-error/10894/14. 

### Build the base training image

```bash
ENVIRONMENT=dev bash scripts/build_training_image.sh
```

### Do interactive model training and data exploration in the Jupyter notebook

```bash
ENVIRONMENT=dev bash scripts/run_training_container.sh
```

Then open [http://localhost:8888](http://localhost:8888).

### Train a model programmatically

```bash
ENVIRONMENT=dev RUNID=`date +%Y%m%d` bash scripts/run_training_container.sh scripts/train.sh
```

## Resources

* https://github.com/pypa/sampleproject/blob/master/setup.py