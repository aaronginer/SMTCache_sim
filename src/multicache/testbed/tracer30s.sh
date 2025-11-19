#!/bin/bash

./pmc_setup.sh
./servers.sh stopall

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

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 50s $3 $4 $5 $6 $7 $8 &

    sleep 15

    trace.sh l1e3 1000000 8 30s ${path}${name}_lm_30s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stop $3 $4 $5 $6 $7 $8
}

go2 () {
  echo "Starting benchmark of $2"
  path=$1
  name=$2

  i=58
  max_loops=100

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $3 $4 $5 $6 $7 $8

    sleep 10

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 50s $3 $4 $5 $6 $7 $8 &

    sleep 15

    trace.sh l1e3 1000000 8 30s ${path}${name}_lm_30s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stop $3 $4 $5 $6 $7 $8
}

#go /media/arn/GODxSSD2/Traces/ cc_app_db app db
#go2 /media/arn/GODxSSD2/Traces/ cc_app_file app file
#go /media/arn/GODxSSD2/Traces/ cc_db_mail db mail
#go2 /media/arn/GODxSSD2/Traces/ cc_db_web db web
#go2 /media/arn/SSD/Traces/ cc_file_web file web
#go2 /media/arn/SSD/Traces/ cc_stream_web stream web


#go2 /media/arn/GODxSSD2/Traces/ cc_db_stream_web db stream web
#go2 /media/arn/GODxSSD2/Traces/ cc_db_file_web db file web
go2 /media/arn/GODxSSD2/Traces/ cc_app_db_web app db web
