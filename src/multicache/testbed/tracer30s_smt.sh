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
    ./servers.sh start $3 $4

    sleep 10

    taskset -c 1 ./runBenchmarks.sh 127.0.0.1 50s $3 &
    taskset -c 2 ./runBenchmarks.sh 127.0.0.1 50s $4 &

    sleep 15

    trace.sh l1e3 1000000 88 30s ${path}${name}_lm_smt_30s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

go2 () {
  echo "Starting benchmark of $2"
  path=$1
  name=$2

  i=0
  max_loops=20

  while [ $i -lt $max_loops ]
  do
    ./servers.sh stopall
    ./servers.sh start $3 $4

    sleep 10

    taskset -c 1 ./runBenchmarks.sh 127.0.0.1 50s $3 &
    taskset -c 2 ./runBenchmarks.sh 127.0.0.1 50s $4 &

    sleep 15

    trace.sh l1e3 1000000 88 30s ${path}${name}_lm_smt_30s_${i}.b

    wait

    ((i++))
  done

  ./servers.sh stopall
}

####  same benchmarks smt (change mail server affinity mask to 88)

#./servers.sh cpuaffinity file 3,7
#go /media/arn/GODxSSD2/Traces/ file_file file

#./servers.sh cpuaffinity web 3,7
#go /media/arn/GODxSSD2/Traces/ web_web web

#./servers.sh cpuaffinity file 3,7
#go /media/arn/GODxSSD2/Traces/ mail_mail mail

#### benchmark combons smt (change mail server affinity mask to 80 and always use cpu7 for mail)

./servers.sh cpuaffinity app 3
./servers.sh cpuaffinity db 7
go2 /media/arn/GODxSSD2/Traces/ app_db app db

./servers.sh cpuaffinity app 3
./servers.sh cpuaffinity file 7
go2 /media/arn/GODxSSD2/Traces/ app_file app file

./servers.sh cpuaffinity app 3
./servers.sh cpuaffinity mail 7
go2 /media/arn/GODxSSD2/Traces/ app_mail app mail

./servers.sh cpuaffinity app 3
./servers.sh cpuaffinity stream 7
go2 /media/arn/GODxSSD2/Traces/ app_stream app stream

./servers.sh cpuaffinity app 3
./servers.sh cpuaffinity web 7
go2 /media/arn/GODxSSD2/Traces/ app_web app web

./servers.sh cpuaffinity db 3
./servers.sh cpuaffinity file 7
go2 /media/arn/GODxSSD2/Traces/ db_file db file

./servers.sh cpuaffinity db 3
./servers.sh cpuaffinity mail 7
go2 /media/arn/GODxSSD2/Traces/ db_mail db mail

./servers.sh cpuaffinity db 3
./servers.sh cpuaffinity stream 7
go2 /media/arn/GODxSSD2/Traces/ db_stream db stream

./servers.sh cpuaffinity db 3
./servers.sh cpuaffinity web 7
go2 /media/arn/GODxSSD2/Traces/ db_web db web

./servers.sh cpuaffinity file 3
./servers.sh cpuaffinity mail 7
go2 /media/arn/GODxSSD2/Traces/ file_mail file mail

./servers.sh cpuaffinity file 3
./servers.sh cpuaffinity stream 7
go2 /media/arn/GODxSSD2/Traces/ file_stream file stream

./servers.sh cpuaffinity file 3
./servers.sh cpuaffinity web 7
go /media/arn/GODxSSD2/Traces/ file_web file web

./servers.sh cpuaffinity mail 7
./servers.sh cpuaffinity stream 3
go /media/arn/GODxSSD2/Traces/ mail_stream mail stream

./servers.sh cpuaffinity mail 7
./servers.sh cpuaffinity web 3
go /media/arn/GODxSSD2/Traces/ mail_web mail web

./servers.sh cpuaffinity stream 3
./servers.sh cpuaffinity web 7
go /media/arn/GODxSSD2/Traces/ stream_web stream web

