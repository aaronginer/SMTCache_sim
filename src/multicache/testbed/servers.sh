#!/bin/bash

function printError {
    echo "Usage: sudo ./servers.sh [options]"
    echo "  - status"
    echo "  - stopall"
    echo "  - startall"
    echo "  - start [server list]                (anyof {app,db,file,mail,stream,web})"
    echo "  - stop  [server list]                (anyof {app,db,file,mail,stream,web})"
    echo "  - cpuaffinity [server] [affinity] (comma seperated list of cpus)"
}

function printStatus {
    if [ "$1" -eq "1" ]; then
        echo "  [Active]"
    else
        echo "  [Inactive]"
    fi
}

if [ "$1" = "status" ]; then
    echo "Checking App-Server..."
    printStatus $(service tomcat9 status | grep "\sactive" | wc -l)

    echo "Checking MySQL-Server..."
    printStatus $(service mysql status | grep "\sactive" | wc -l)

    echo "Checking File-Server..."
    printStatus $(service smbd status | grep "\sactive" | wc -l)

    echo "Checking Mail-Server..."
    printStatus $(service postfix status | grep "\sactive" | wc -l)

    echo "Checking Streaming-Server..."
    printStatus $(service ffserver status | grep "\sactive" | wc -l)

    echo "Checking Web-Server..."
    printStatus $(service apache2 status | grep "\sactive" | wc -l)
elif [ "$1" = "stopall" ]; then
    service tomcat9 stop
    service mysql stop
    service smbd stop
    service postfix stop
    service ffserver stop
    service apache2 stop
elif [ "$1" = "startall" ]; then
    service tomcat9 start
    service mysql start
    service smbd start
    service postfix start
    service ffserver start
    service apache2 start
elif [[ "$1" = "start" && "$#" -ge "2" ]]; then
    for arg in ${@:2}
    do
        # check if directory exists that corresponds to argument name
        if [ ! -d "$arg" ]; then
            echo "'$arg' is not a valid server"
            continue
        fi
        # run target benchmark

        echo "Starting $arg server..."
        ./$arg/server/start.sh
    done
elif [[ "$1" = "stop" && "$#" -ge "2" ]]; then
    for arg in ${@:2}
    do
        # check if directory exists that corresponds to argument name
        if [ ! -d "$arg" ]; then
            echo "'$arg' is not a valid server"
            continue
        fi
        # run target benchmark

        echo "Stopping $arg server..."
        ./$arg/server/stop.sh
    done
elif [[ "$1" = "cpuaffinity" && "$#" -ge "3" ]]; then
    affinity=$(echo "$3" | grep -x -E "([0-9],)*[0-9]")
    if [ ! -d "$2" ]; then
        echo "'$arg' is not a valid server"
    elif [ "$affinity" == "" ]; then
        echo "Affinity invalid. Format = ([0-9],)*[0-9]"
    else
        echo "Setting CPUAffinity for $2 to $3"
        ./$2/server/cpuaffinity.sh $3
    fi
else
    printError
fi