#!/usr/bin/env python

import sys
import argparse

#assuming that we're comparing to 1KG sample with all of the genotypes as the a file.

class StrandFilter(object):
    def __init__(self, allowable_tuples):
        self.allowable_strands = set(allowable_tuples)

    def __call__(self, compare_strand_a, compare_strand_b):
        if (compare_strand_a, compare_strand_b) in self.allowable_strands:
            return True
        else:
            return False

class OneThousandGenomesIntersect(object):
    def __init__(self):
        self.filters = {
                'DEL': StrandFilter([('+', '-')]),
                'MEI': StrandFilter([('+', '-')]),
                'DUP': StrandFilter([('-', '+')]),
                'INV': StrandFilter([('-', '-'), ('+', '+')]),
                # We don't want to compare to these
                # Commenting out so we can check that we've succesfully removed them from input files
                #'CNV': StrandFilter([(None, None)]),
                #'INS': StrandFilter([(None, None)]),
                #'ALU': StrandFilter([(None, None)]),
                #'LINE1': StrandFilter([(None, None)]),
                #'SVA': StrandFilter([(None, None)])
                }
    def __call__(self, onekg_type, compare_strand_a, compare_strand_b):
        try:
            return self.filters[onekg_type](compare_strand_a, compare_strand_b)
        except KeyError:
            raise ValueError("Unexpected type {0}".format(onekg_type))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter output of pairtopair based on strand.')
    parser.add_argument('-n', '--num-first-sample', metavar='<INT>', type=int, help='Number of columns in the -a file passed to pairtopair')
    args = parser.parse_args()

    type_index = 10
    first_callset_index = args.num_first_sample
    strand_a_index = 8
    strand_b_index = 9
    
    hit_in_onekg = OneThousandGenomesIntersect()

    try:
        for line in sys.stdin:
            fields = line.rstrip().split('\t')
            if hit_in_onekg(fields[type_index], fields[first_callset_index + strand_a_index], fields[first_callset_index + strand_b_index]):
                print line,
    except ValueError as e:
        sys.exit(e)

