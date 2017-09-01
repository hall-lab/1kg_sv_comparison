#!/usr/bin/env python

import vcf

import argparse
import sys

class TypeConverter(object):
    '''
    Translates the 1KG type to it's corresponding type in the svtools workflow.
    Note that these are a hardcoded lookup table for future safety
    '''

    # The following is our hard coded lookup table
    svtools_type = { 
            'ALU': 'ALU',
            'CNV': 'CNV',
            'DEL': 'DEL',
            'DEL_ALU': 'MEI',
            'DEL_HERV': 'MEI',
            'DEL_LINE1': 'MEI',
            'DEL_SVA': 'MEI',
            'DUP': 'DUP',
            'INS': 'INS',
            'INV': 'INV',
            'LINE1': 'LINE1',
            'SVA': 'SVA'
            }

    def __call__(self, record):
        try:
            svtype = record.INFO['SVTYPE']
        except KeyError:
            sys.exit('VCF file must contain SVTYPE fields for every line')
        try:
            record.INFO['SVTYPE'] = self.svtools_type[svtype]
        except KeyError:
            sys.exit('Unexpected SVTYPE: {0}'.format(svtype))
        return record

def create_parser():
    parser = argparse.ArgumentParser(description='Convert the SVTypes in a 1000 Genomes Phase 3 SV call set VCF to be compatible with svtools')
    parser.add_argument('input', metavar='<VCF>', type=argparse.FileType('rb'), nargs='?', default=None, help='File to process (use - for stdin)')
    parser.add_argument('--output', metavar='<VCF>', action='store', default=sys.stdout, help='Filename to write output to [stdout]')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    vcf_input = vcf.Reader(args.input)
    vcf_output = vcf.Writer(args.output, vcf_input)

    translate = TypeConverter()

    for entry in vcf_input:
        entry = translate(entry)
        vcf_output.write_record(entry)

if __name__ == '__main__': 
    main()
