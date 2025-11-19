#!/bin/bash

echo "Running app-server benchmark with timeout=${2} and IP=${1}..."

ab -t $2 -n 100000000 -c 32 http://${1}:8080/examples/jsp/dates/date.jsp