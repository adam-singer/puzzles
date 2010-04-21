#!/bin/bash

python2.5 index.py twl06.txt
mkdir -p dist
tar zcf dist/breathalyzer.tar.gz `cat manifest.txt`
