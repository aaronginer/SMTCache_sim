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
        python3 parse_ssv.py --file ${FOLDER_PREFIX}${TRACE_PREFIX}_${i}.b --cpc $CPC --lc 8 --pc 4 --target_core 3 --export &
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

#export_traces /media/arn/GODxSSD2/Traces/ file_file_ssv_smt_30s 5 5
#export_traces /media/arn/GODxSSD2/Traces/ web_web_ssv_smt_30s 5 5
#export_traces /media/arn/GODxSSD2/Traces/ mail_mail_ssv_smt_30s 5 5

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ app_mail_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ app_stream_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ app_web_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ file_mail_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ file_stream_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ mail_stream_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ mail_web_ssv_smt_30s 3 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_smt_30s 3 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ app_mail_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ app_stream_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ app_web_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ file_mail_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ file_stream_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ mail_stream_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ mail_web_ssv_smt_30s 4 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_smt_30s 4 50

export_traces /media/arn/GODxSSD2/Traces/ app_db_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ app_file_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ app_mail_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ app_stream_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ app_web_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_file_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_mail_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_stream_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ db_web_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ file_mail_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ file_stream_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ file_web_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ mail_stream_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ mail_web_ssv_smt_30s 5 50
export_traces /media/arn/GODxSSD2/Traces/ stream_web_ssv_smt_30s 5 50