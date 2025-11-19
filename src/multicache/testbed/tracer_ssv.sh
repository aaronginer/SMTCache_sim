#!/bin/bash

./pmc_setup.sh

go () {
  echo "Starting benchmark of $2"
  path=$1
  test=$2
  prefix=$3

  i=0
  max_loops=10

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $test

    sleep 10

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 20s $test &

    sleep 10

    trace.sh ssv 50000 8 5s ${path}${prefix}${test}_lm_5s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

go ./ app
go ./ db
go ./ file
go ./ mail
go ./ stream
go ./ web
