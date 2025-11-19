#!/bin/bash

./pmc_setup.sh

go () {
  echo "Starting benchmark of $2"
  path=$1
  name=$2

  i=30
  max_loops=100

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $3 $4 $5 $6 $7 $8

    sleep 10

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 40s $3 $4 $5 $6 $7 $8 &

    sleep 20

    trace.sh l1e2 1000000 8 5s ${path}${name}_lm_5s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

go /media/arn/GODxSSD2/Traces/ app app
go /media/arn/GODxSSD2/Traces/ db db
go /media/arn/GODxSSD2/Traces/ file file
go /media/arn/GODxSSD2/Traces/ mail mail
go /media/arn/GODxSSD2/Traces/ stream stream
go /media/arn/GODxSSD2/Traces/ web web
