#!/bin/sh
virtualenv .
./bin/pip install setuptools==33.1.1
./bin/pip install zc.buildout==2.12.0
./bin/pip install -r requirements.txt

