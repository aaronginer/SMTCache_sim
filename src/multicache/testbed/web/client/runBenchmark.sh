#!/bin/bash

echo "Running web-server benchmark with timeout=${2} and IP=${1}..."

ab -t $2 -n 20000000 -c 32 http://${1}:80/