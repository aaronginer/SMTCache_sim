#!/bin/bash

FOLDER=$1
FILTER=$2

export_traces () {
    FOLDER_PREFIX=$1
    TRACE_PREFIX=$2
    MAX_LOOPS=$3

    i=0

    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 parse_l1e.py --file ${FOLDER_PREFIX}${TRACE_PREFIX}_${i}.b --cores 4 --events miss hit inst --target_core 3 --export &
        ((i++))
    done

    wait

    mkdir ${FOLDER_PREFIX}${TRACE_PREFIX}

    i=0
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        mv ${FOLDER_PREFIX}${TRACE_PREFIX}_${i} ${FOLDER_PREFIX}${TRACE_PREFIX}
        ((i++))
    done

    i=0
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 split_export.py ${FOLDER_PREFIX}${TRACE_PREFIX}/${TRACE_PREFIX}_${i}/
        ((i++))
    done
}

export_traces /media/arn/GODxSSD2/Traces/ norestart_app_lm_5s 100