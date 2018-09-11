#!/bin/sh

cd src
for d in */ ; do
    cd "$d"
    if [ -f "docs.py" ]
    then
        echo "Start docs.py tests in $d"
        ../../bin/nosetests docs.py
    fi
    cd ..
done