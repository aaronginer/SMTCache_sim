#!/bin/bash

# benchmarking mail only works within local network for now

# https://serverfault.com/questions/393630/how-can-i-stress-test-my-postfix-system-without-actually-sending-existing-addess

echo "Running mail-server benchmark with timeout=${2} and IP=${1}..."

                                                                          # probably have to change this to public IP if I want to use this with public IP
# timeout -k 1s ${2}s smtp-source -s 32 -l 512000 -m 1000000 -c -R 1 -f root@$(hostname -i) -t root@${1} ${1}
timeout -k 1s ${2}s smtp-source -s 32 -l 5120 -m 1000000 -c -R 1 -f root@$(hostname -i) -t root@${1} ${1}


rm /var/mail/root
