#!/usr/bin/env python

import vcf

import argparse
import sys

class PassFilter(object):
    def __call__(self, id_list):
        return True

class FailFilter(object):
    def __call__(self, id_list):
        return False

class DeletionFilter(object):
    def __init__(self):
        self.exclude_prefixes = ( 'YL_CN_', 'BI_GS_CNV_', 'BI_GS_DEL', 'DUP_uwash_' )
        self.include_prefixes = ( 'SI_BD', 'EM_DL_', 'DEL_pindel', 'UW_VH_' )

    def should_include(self, var_id):
        return var_id.startswith(self.include_prefixes)

    def should_exclude(self, var_id):
        return var_id.startswith(self.exclude_prefixes)

    def __call__(self, id_list):
        # this will be slow, but let's be safe
        all_ids = set(id_list)
        exclude = set(filter(self.should_exclude, id_list))
        include = set(filter(self.should_include, id_list))
        unhandled = all_ids - exclude - include
        if unhandled:
            unhandled_ids = ','.join([ x for x in unhandled ])
            raise RuntimeError('Unexpected id(s): {0}'.format(unhandled_ids))

        if exclude & include:
            raise RuntimeError('Matched an id in both the exclude and include lists')
        else:
            return bool(include)

class EntryFilter(object):
    def __init__(self):
        self.callset_filter_lut = {
            'ALU_umary': FailFilter(),
            'L1_umary': FailFilter(),
            'SVA_umary': FailFilter(),
            'NUMT_umich': FailFilter(),
            'DEL_union': DeletionFilter(),
            'DEL_pindel': PassFilter(),
            'INV_delly': PassFilter(),
            'CINV_delly': PassFilter(),
            'DUP_gs': FailFilter(),
            'DUP_delly': PassFilter(),
            'DUP_uwash': FailFilter()
            }

    def __call__(self, cs_tag, var_id, mc_tag):
        filter_func = self.callset_filter_lut[cs_tag]
        var_list = [var_id]
        if mc_tag:
            var_list.extend(mc_tag)
        return filter_func(var_list)
        
def create_parser():
    parser = argparse.ArgumentParser(description='Remove calls from 1000 Genomes Phase 3 SV call set that only came from read-depth based algorithms or were insertions.')
    parser.add_argument('input', metavar='<VCF>', type=argparse.FileType('rb'), nargs='?', default=None, help='File to process (use - for stdin)')
    parser.add_argument('--output', metavar='<VCF>', action='store', default=sys.stdout, help='Filename to write output to [stdout]')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    vcf_input = vcf.Reader(args.input)
    vcf_output = vcf.Writer(args.output, vcf_input)

    callset_filter = EntryFilter()

    for entry in vcf_input:
        try:
            cs = entry.INFO['CS']
        except KeyError:
            sys.exit('VCF file must contain CS tags on every line')

        mc = None
        try:
            mc = entry.INFO['MC']
        except KeyError:
            pass
            
        if callset_filter(cs, entry.ID, mc):
            vcf_output.write_record(entry)

if __name__ == '__main__': 
    main()
