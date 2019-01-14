import os
import pickle
import re

import boto3
import botocore


def get_s3_keys(bucket, Prefix=None):
    """Get a list of keys in an S3 bucket."""
    client = boto3.client('s3')

    keys = []
    resp = client.list_objects_v2(Bucket=bucket, MaxKeys=100000, Prefix=Prefix)
    if 'Contents' in resp:
        for obj in resp['Contents']:
            keys.append(obj['Key'])
    return keys


def get_latest_s3_dateint(datadir=None, bucket=None):
    all_keys = get_s3_keys(bucket, Prefix=datadir)
    latest_dateint = None
    for subdir in all_keys:
        m = re.search(datadir + r'/(\d{8})', subdir)
        if m:
            dateint = m.group(1)
            if latest_dateint is None or dateint > latest_dateint:
                latest_dateint = dateint
    if latest_dateint is None:
        raise RuntimeError("No dateint directories found in {}/{}/".format(bucket, datadir))
    return latest_dateint


def load_from_s3(filename=None, subdirectory=None, bucket=None):
    response = None

    if filename is None:
        raise ValueError("You must specify a filename")
    if subdirectory is None:
        raise ValueError("You must specify a subdirectory")

    client = boto3.client('s3')

    try:
        response = client.get_object(Bucket=bucket, Key=subdirectory + '/' + filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The obj does not exist.")
        else:
            raise

    obj_bytes = response['Body'].read()

    return obj_bytes


def load_from_s3_and_unpickle(filename=None, subdirectory=None, bucket=None):
    if filename is None:
        raise ValueError("You must specify a filename")
    if subdirectory is None:
        raise ValueError("You must specify a subdirectory")

    obj_bytes = load_from_s3(filename=filename, subdirectory=subdirectory, bucket=bucket)

    obj = pickle.loads(obj_bytes)

    return obj


def pickle_to_fs(obj=None, filename=None, subdirectory=None):
    if obj is None:
        raise ValueError("You must specify an obj")
    if filename is None:
        raise ValueError("You must specify a filename")
    if subdirectory is None:
        raise ValueError("You must specify a subdirectory")

    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    with open(os.path.join(subdirectory, filename), 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)


def download_glove():
    url = "http://www-nlp.stanford.edu/data/glove.840B.300d.zip"
