#!/bin/bash
# server side script to trace context switch information as well as optionally performance counter information

PERF=0
TIMEOUT=0
FILE=""

function usage {
    echo "Usage: ./runBenchmark {event} {buffer_size_kb} {timeout[s,m]} {file} (perf)*"
    echo "   event                   - available: ssv, l1e, etc."
    echo "   buffer_size_kb          - per-core trace buffer size" 
    echo "   tracing_cpumask         - single digit hex, set bit = tracing enabled (1-f)"
    echo "   timeout                 - timeout for trace and perf"
    echo "   file                    - file path where to save trace (absolute)"
    exit -1
}

function convertTimeout {
    # check valid timeout format
    grep -E -q "^[1-9][0-9]*(s|m)$" <<< $1
    if [ ! "$?" -eq "0" ]; then
        echo "Invalid timeout format"
        usage
    fi

    grep -E -q "^[1-9][0-9]*m$" <<< $1

    if [ ! "$?" -eq "0" ]; then
        echo "$(grep -o "[1-9][0-9]*" <<< $1)"
    else
        echo "$(($(grep -o "[1-9][0-9]*" <<< $1) * 60))"
    fi
}

function _setup {
    # $1 = buffer_size_kb
    grep -E -q "^[1-9][0-9]+$" <<< $1
    if [ "$?" -eq "1" ]; then
        echo "Invalid buffer size"
        exit -1
    elif [ "$1" -le "20000" ]; then
        echo "Buffer size too small"
        exit -1
    fi
    echo "Setting buffer size fore cores {$2} to $1 kb."

    HEX_MASK="0x$2"
    # core 0
    if [ "$(($HEX_MASK & 0x1))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu0/buffer_size_kb
    fi
    # core 1
    if [ "$(($HEX_MASK & 0x2))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu1/buffer_size_kb
    fi
    #core 2
    if [ "$(($HEX_MASK & 0x4))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu2/buffer_size_kb
    fi
    #core 3
    if [ "$(($HEX_MASK & 0x8))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu3/buffer_size_kb
    fi
    # core 4
    if [ "$(($HEX_MASK & 0x10))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu4/buffer_size_kb
    fi
    # core 5
    if [ "$(($HEX_MASK & 0x20))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu5/buffer_size_kb
    fi
    # core 6
    if [ "$(($HEX_MASK & 0x40))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu6/buffer_size_kb
    fi
    # core 7
    if [ "$(($HEX_MASK & 0x80))" != 0 ]; then
        echo $1 >> /sys/kernel/debug/tracing/per_cpu/cpu7/buffer_size_kb
    fi
    echo "Buffers created."
    echo "Setting tracing mask to $2"
    echo $2 >> /sys/kernel/debug/tracing/tracing_cpumask
    echo "Tracing mask set"
}

function _trace {
    echo "Enabling trace event."
    echo $EVENT >> /sys/kernel/debug/tracing/set_event
    sleep $TIMEOUT
    echo "!$EVENT" >> /sys/kernel/debug/tracing/set_event
    echo "Disabling event."
    echo "Copying data to trace file $FILE"
    cp /sys/kernel/debug/tracing/trace $FILE
    echo "" > /sys/kernel/debug/tracing/trace
    echo "Trace task finished."
}

# check length
if [ "$#" -le "2" ]; then
    usage
fi

# check file path (TODO)
EVENT=$1
TIMEOUT=$(convertTimeout $4)
FILE=$5

_setup $2 $3
_trace &

wait

echo "Tracing finished."

