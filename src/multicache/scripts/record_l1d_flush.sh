#!/bin/bash

record () {
  PREFIX=$1
  RUNS=$2
  SETS=$3
  i=0

  gcc -o mbench_l1_flush mbench_l1_flush.c -DUSE_SETS=$3

  while [ $i -lt $RUNS ]
  do
    taskset -c 3 ./mbench_l1_flush >> ${PREFIX}_l1d_flush_${SETS}.b
    echo ${PREFIX}_${SETS}_$i
    ((i++))
  done
}

record normal 666 0
record normal 666 16
record normal 666 32
record normal 666 48
record normal 666 64

