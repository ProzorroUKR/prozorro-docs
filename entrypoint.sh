#!/usr/bin/env bash

cd /app
./bootstrap.sh
./bin/buildout -c develop.cfg
sleep infinity