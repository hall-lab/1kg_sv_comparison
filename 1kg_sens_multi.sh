#!/bin/bash

set -ueo pipefail

OKG_VCF=$1
EVAL_VCF=$2
MAP=$3
GENOME=$4

BINDIR=$( dirname $0 )
SENS_SCRIPT=${BINDIR}/1kg_sens.sh
SVTOOLS=svtools
BCFTOOLS=bcftools

while read INTERNAL EXTERNAL
do
    echo $EXTERNAL
    mkdir $EXTERNAL
    OKG_BEDPE=$EXTERNAL/1kg_$EXTERNAL.bedpe
    EVAL_BEDPE=$EXTERNAL/$INTERNAL.var_only.bedpe
    $BCFTOOLS view -s $EXTERNAL --min-ac 1 $OKG_VCF | $SVTOOLS vcftobedpe | $SVTOOLS bedpesort > $OKG_BEDPE
    $BCFTOOLS view -s $INTERNAL --min-ac 1 $EVAL_VCF | $SVTOOLS vcftobedpe | $SVTOOLS bedpesort > $EVAL_BEDPE
    bash $SENS_SCRIPT $OKG_BEDPE $EVAL_BEDPE $GENOME > $EXTERNAL/$EXTERNAL.1kg.sensitivity
done < $MAP

