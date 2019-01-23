try:
    import unzip_requirements
except ImportError:
    pass

import os
import json
import logging

from pmip.data import load_from_s3_and_unpickle, get_latest_s3_dateint

model_id = get_latest_s3_dateint(datadir='models', bucket=os.getenv('BUCKET'))
model = load_from_s3_and_unpickle(filename='model.pkl', subdirectory=f'models/{model_id}', bucket=os.getenv('BUCKET'))


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def healthcheck(event, context):
    body = {
        "status": "ok"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def predict(event, context):
    request_data = json.loads(event['body'])

    if 'queryStringParameters' in event:
        if 'flavor' in event['queryStringParameters']:
            flavor = event['queryStringParameters']['flavor']
    else:
        flavor = None

    if 'comments' not in request_data:
        logging.error("You must provide a list of comments in the data payload")
        raise Exception("You must provide a list of comments in the data payload")
        return

    if flavor is None or flavor == 'class':
        val = model.predict(request_data['comments'])
        prediction = [{'class': int(s)} for s in val]
    elif flavor == 'probability':
        val = model.predict_proba(request_data['comments'])
        prediction = [{'probability': list(s)} for s in val]
    else:
        logging.error(f"Unknown type {flavor}")
        raise Exception(f"Unknown type {flavor}")
        return

    body = {
        'prediction': prediction
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response


def get_test(event, context):
    val = model.predict(["Check it out this free stuff!!!", "I take issue with your characterization."])
    prediction = [{'class': int(s)} for s in val]

    body = {'prediction': prediction}

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response
