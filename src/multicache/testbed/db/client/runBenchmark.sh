#!/bin/bash

echo "Running db-server benchmark with timeout=${2} and IP=${1}..."

sysbench --db_driver=mysql --mysql-host=${1} --mysql_user=mysql_test_user --mysql-db=mysql_test_db --mysql-password=mysql_test_pw --table_size=100000 --tables=2 --threads=1 --events=0 /usr/share/sysbench/oltp_read_only.lua prepare
sysbench --time=${2} --db_driver=mysql --mysql-host=${1} --mysql_user=mysql_test_user --mysql-db=mysql_test_db --mysql-password=mysql_test_pw --table_size=100000 --tables=2 --threads=32 --events=0 /usr/share/sysbench/oltp_read_only.lua run