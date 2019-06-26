#!/bin/sh
virtualenv -p python2.7 venv

./venv/bin/pip install -r requirements.txt

git clone https://github.com/ProzorroUKR/openprocurement.api.git src/openprocurement.api
./venv/bin/pip install -r src/openprocurement.api/requirements.txt
./venv/bin/pip install -e src/openprocurement.api/
