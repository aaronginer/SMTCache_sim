#!/bin/bash

echo "Running file-server benchmark with timeout=${2}, IP=${1}..."

USERNAME="arn"
PASSWORD="password"

FILE_WRITE="file/client/smb-write-files.txt"
FILE_READ="file/client/smb-read-files.txt"

dbench 32 -t ${2} -B smb --smb-share=//${1}/sambashare --smb-user=$USERNAME%$PASSWORD --loadfile=$FILE_WRITE 2
