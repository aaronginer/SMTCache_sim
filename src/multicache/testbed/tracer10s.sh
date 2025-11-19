#!/bin/bash

./pmc_setup.sh

go () {
  echo "Starting benchmark of $2"
  path=$1
  name=$2

  i=0
  max_loops=100

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $3 $4 $5 $6 $7 $8

    sleep 10

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 40s $3 $4 $5 $6 $7 $8 &

    sleep 20

    trace.sh l1e3 1000000 8 10s ${path}${name}_lm_10s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

go /media/arn/GODxSSD2/Traces/ app_db app db
