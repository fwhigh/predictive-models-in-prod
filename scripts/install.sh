#!/usr/bin/env bash

if [ "$ENVIRONMENT" == "prod" ]; then
    echo "Installing pmip package in prod environment"
    pip install -U --upgrade-strategy only-if-needed -e .
elif [ "$ENVIRONMENT" == "staging" ]; then
    echo "Installing pmip package in staging environment"
    pip install -U --upgrade-strategy only-if-needed .
else
    echo "Installing pmip package in dev environment"
    pip install -U --upgrade-strategy only-if-needed .
fi