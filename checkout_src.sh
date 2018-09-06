#!/bin/sh

if [ -z "$1" ]
then
    echo "No branch supplied (Example: './checkout_src.sh feature/mind-blow')"
    exit
fi

cd src
for d in */ ; do
    cd "$d"
    git checkout "$1" && echo "Success $d" || echo "Fail $d"
    cd ..
done