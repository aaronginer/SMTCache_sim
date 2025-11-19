#!/bin/bash

function usage {
    echo "Usage: ./runBenchmark {IP} {timeout[s,m]} {test1} {test2} ..."
    exit -1
}

function convertTimeout {
    grep -E -q "^[1-9][0-9]*m$" <<< $1

    if [ ! "$?" -eq "0" ]; then
        echo "$(grep -o "[1-9][0-9]*" <<< $1)"
    else
        echo "$(($(grep -o "[1-9][0-9]*" <<< $1) * 60))"
    fi
}

# check length
if [ "$#" -le "2" ]; then
    usage
fi

grep -E -q '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$' <<< $1

# check valid IP format
if [ ! "$?" -eq "0" ]; then
    echo "Invalid IP format"
    usage
fi

grep -E -q "^[1-9][0-9]*(s|m)$" <<< $2

# check valid timeout format
if [ ! "$?" -eq "0" ]; then
    echo "Invalid timeout format"
    usage
fi

mkdir -p results

# loop through arguments starting at the fourth
for arg in ${@:3}
do
    # check if directory exists that corresponds to argument name
    if [ ! -d "$arg" ]; then
        echo "'$arg' is not a valid test"
        continue
    fi
    # run target benchmark

    ./$arg/client/runBenchmark.sh $1 $(convertTimeout $2) &> results/${arg}_$(date +%m%d%Y-%H%M%S).log & # run in background
done

wait

echo "Benchmark finished."