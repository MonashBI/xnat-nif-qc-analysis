#!/usr/bin/env bash

# Map bash arguments to local variables
export SESSION=$1
export T1=$2
export T2=$3
export DMRI=$4

# Derive instrument ID and date from session id
export SUBJECT=${SESSION%_*}
export INSTRUMENT=${SUBJECT#*_}
export DATE=${SESSION##*_}

# Run the analysis script
echo /usr/bin/python /repo/scripts/qc_analysis.py \
                $XNAT_HOST \
                --phantom t1_32ch "$T1" \
                --phantom t2_32ch "$T2" \
                --phantom dmri_32ch "$DMRI" \
                --dates "$DATE" \
                --instrument "$INSTRUMENT" \
                --work_dir /workdir \
                --auth "$XNAT_USER" "$XNAT_PASS"
/usr/bin/python /repo/scripts/qc_analysis.py \
                $XNAT_HOST \
                --phantom t1_32ch "$T1" \
                --phantom t2_32ch "$T2" \
                --phantom dmri_32ch "$DMRI" \
                --dates "$DATE" \
                --instrument "$INSTRUMENT" \
                --work_dir /workdir \
                --auth "$XNAT_USER" "$XNAT_PASS"                                  
