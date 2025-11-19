#!/bin/bash

go () {
  echo "Starting benchmark of $2"
  path=$1
  name=$2

  i=0
  max_loops=50

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $3 $4 $5 $6 $7 $8

    sleep 10

    taskset -c 1,2 ./runBenchmarks.sh 127.0.0.1 50s $3 $4 $5 $6 $7 $8 &

    sleep 15

    trace.sh ssv 1000000 8 30s ${path}${name}_ssv_30s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

#go /media/arn/GODxSSD2/Traces/ app_db app db
#go /media/arn/GODxSSD2/Traces/ app_file app file
#go /media/arn/GODxSSD2/Traces/ db_mail db mail
#go /media/arn/GODxSSD2/Traces/ db_web db web
#go /media/arn/GODxSSD2/Traces/ file_web file web
#go /media/arn/GODxSSD2/Traces/ stream_web stream web

go /media/arn/GODxSSD2/Traces/ db_stream_web db stream web
go /media/arn/GODxSSD2/Traces/ db_file_web db file web
go /media/arn/GODxSSD2/Traces/ app_db_web app db web
