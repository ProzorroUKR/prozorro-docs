#!/bin/sh

REPO=https://github.com/ProzorroUKR/openprocurement.api.git
DEST=src/openprocurement.api

virtualenv -p python2.7 venv

./venv/bin/pip install -r requirements.txt

git clone --branch ${BRANCH:-master} ${REPO} ${DEST} || git clone ${REPO} ${DEST}

./venv/bin/pip install -r $DEST/requirements.txt
./venv/bin/pip install -e $DEST/
