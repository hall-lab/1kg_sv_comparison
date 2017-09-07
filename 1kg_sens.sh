#!/bin/bash

set -ueo pipefail

OKG_BEDPE=$1
EVAL_BEDPE=$2

SLOP=50
SLOP=$(( ${SLOP} - 1)) # adjust slop so we get a single overall value
BINDIR=$( dirname $0 )

INTERSECT_SCRIPT=${BINDIR}/filter_based_on_strand.py
BEDTOOLS=bedtools
PYTHON=python

TOTAL_1KG=$(cat $OKG_BEDPE | grep -v '^#' | wc -l)
TOTAL_UNFILTERED=$(cat $EVAL_BEDPE | grep -v '^#' | wc -l)
TOTAL_FILTERED=$(cat $EVAL_BEDPE | grep -v '^#' | awk '{ if ($12 != "LOW") { print }}' | wc -l)
OVERLAP_UNFILTERED=$(cat $EVAL_BEDPE | perl -ape 'if($_ !~ /^#/) { $F[1]-=1; $F[2]+=1; $F[4]-=1; $F[5]+=1; @F[1,4] = map { $_ < 0 ? 0 : $_ } ($F[1], $F[4]); $_=join("\t", @F)."\n"}' | $BEDTOOLS pairtopair -is -type both -slop $SLOP -rdn -a $OKG_BEDPE -b stdin | grep -v '^#' | $PYTHON $INTERSECT_SCRIPT -n 22 | cut -f1-11 | sort -u | wc -l)
OVERLAP_FILTERED=$(cat $EVAL_BEDPE | awk '{ if ($12 == "PASS" || $12 == ".") { print }}' | perl -ape 'if($_ !~ /^#/) { $F[1]-=1; $F[2]+=1; $F[4]-=1; $F[5]+=1; @F[1,4] = map { $_ < 0 ? 0 : $_ } ($F[1], $F[4]); $_=join("\t", @F)."\n"}' | $BEDTOOLS pairtopair -is -type both -slop $SLOP -rdn -a $OKG_BEDPE -b stdin | grep -v '^#' | $PYTHON $INTERSECT_SCRIPT -n 22 | cut -f1-11 | sort -u | wc -l)
FRACTION_UNFILTERED=$(awk "BEGIN { print $OVERLAP_UNFILTERED / $TOTAL_UNFILTERED }")
SENS_UNFILTERED=$(awk "BEGIN { print $OVERLAP_UNFILTERED / $TOTAL_1KG }")
FRACTION_FILTERED=$(awk "BEGIN { print $OVERLAP_FILTERED / $TOTAL_FILTERED }")
SENS_FILTERED=$(awk "BEGIN { print $OVERLAP_FILTERED / $TOTAL_1KG }")

echo -e "Unfiltered Total Calls\t$TOTAL_UNFILTERED"
echo -e "Unfiltered Overlapping 1KG\t$OVERLAP_UNFILTERED"
echo -e "Unfiltered Fraction Overlapping 1KG\t$FRACTION_UNFILTERED"
echo -e "Unfiltered 1KG Sensitivity\t$SENS_UNFILTERED"
echo -e "Filtered Total Calls\t$TOTAL_FILTERED"
echo -e "Filtered Overlapping 1KG\t$OVERLAP_FILTERED"
echo -e "Filtered Fraction Overlapping 1KG\t$FRACTION_FILTERED"
echo -e "Filtered 1KG Sensitivity\t$SENS_FILTERED"
