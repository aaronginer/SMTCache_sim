#!/bin/bash

FOLDER=$1
FILTER=$2

export_traces () {
    FOLDER_PREFIX=$1
    TRACE_PREFIX=$2
    CPC=$3
    MAX_LOOPS=$4

    i=0

    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 parse_ssv.py --file ${FOLDER_PREFIX}${TRACE_PREFIX}_${i}.b --cpc $CPC --lc 4 --pc 4 --target_core 3 --export &
        ((i++))
    done

    wait

    mkdir ${FOLDER_PREFIX}${TRACE_PREFIX}_cpc${CPC}

    i=0
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        mv ${FOLDER_PREFIX}${TRACE_PREFIX}_${i} ${FOLDER_PREFIX}${TRACE_PREFIX}_cpc${CPC}
        ((i++))
    done

    i=0
    while [ "$i" -lt "$MAX_LOOPS" ]
    do
        python3 split_export.py ${FOLDER_PREFIX}${TRACE_PREFIX}_cpc${CPC}/${TRACE_PREFIX}_${i}/
        ((i++))
    done
}

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_30s 3 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_30s 4 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_30s 5 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_web_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_web_ssv_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_web_ssv_30s 3 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_web_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_web_ssv_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_web_ssv_30s 4 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_web_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_web_ssv_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_web_ssv_30s 5 50