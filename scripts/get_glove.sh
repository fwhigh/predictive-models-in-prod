#!/usr/bin/env bash

if [ ! -f "data/glove/glove.840B.300d.txt" ]; then
    wget http://www-nlp.stanford.edu/data/glove.840B.300d.zip
    mkdir -p data/glove
    mv glove.840B.300d.zip data/glove
    unzip data/glove/glove.840B.300d.zip -d data/glove
    rm data/glove/glove.840B.300d.zip
figo