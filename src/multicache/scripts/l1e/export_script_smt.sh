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
        python3 parse_l1e.py --file ${FOLDER_PREFIX}${TRACE_PREFIX}_${i}.b --cores 8 --events miss hit inst --target_core 3 7 --export &
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

export_traces2 () {
    FOLDER_PREFIX=$1
    TRACE_PREFIX=$2
    MAX_LOOPS=$3

    i=20

    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 parse_l1e.py --file ${FOLDER_PREFIX}${TRACE_PREFIX}_${i}.b --cores 8 --events miss hit --target_core 3 7 --export &
        ((i++))
    done

    wait

    mkdir ${FOLDER_PREFIX}${TRACE_PREFIX}

    i=20
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        mv ${FOLDER_PREFIX}${TRACE_PREFIX}_${i} ${FOLDER_PREFIX}${TRACE_PREFIX}
        ((i++))
    done

    i=20
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 split_export.py ${FOLDER_PREFIX}${TRACE_PREFIX}/${TRACE_PREFIX}_${i}/
        ((i++))
    done
}

export_traces /media/arn/GODxSSD2/Traces/ app_db_lm_smt_30s 20

export_traces2 /media/arn/GODxSSD2/Traces/ app_file_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ app_mail_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ app_stream_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ app_web_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ db_file_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ db_mail_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ db_stream_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ db_web_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ file_mail_lm_smt_30s 100
export_traces2 /media/arn/GODxSSD2/Traces/ file_stream_lm_smt_30s 100

export_traces /media/arn/GODxSSD2/Traces/ app_file_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ app_mail_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ app_stream_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ app_web_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ db_file_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ db_mail_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ db_stream_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ db_web_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ file_mail_lm_smt_30s 20
export_traces /media/arn/GODxSSD2/Traces/ file_stream_lm_smt_30s 20


export_traces /media/arn/GODxSSD2/Traces/ file_web_lm_smt_30s 100
export_traces /media/arn/GODxSSD2/Traces/ mail_stream_lm_smt_30s 100
export_traces /media/arn/GODxSSD2/Traces/ mail_web_lm_smt_30s 100
export_traces /media/arn/GODxSSD2/Traces/ stream_web_lm_smt_30s 100