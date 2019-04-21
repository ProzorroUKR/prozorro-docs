#!/bin/sh
virtualenv -p python2.7 .

./bin/pip install -r requirements.txt

git clone https://github.com/ProzorroUKR/openprocurement.api.git src/openprocurement.api
./bin/pip install -r src/openprocurement.api/requirements.txt
./bin/pip install -e src/openprocurement.api/
