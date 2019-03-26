#!/bin/sh
virtualenv -p python2.7 .
#curl https://bootstrap.pypa.io/get-pip.py | ./bin/python  # fixes "There was a problem confirming the ssl certificate: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 a..."
./bin/pip install -r requirements.txt

git clone https://github.com/ProzorroUKR/openprocurement.api.git src/openprocurement.api
./bin/pip install -r src/openprocurement.api/requirements.txt
./bin/pip install -e src/openprocurement.api/
