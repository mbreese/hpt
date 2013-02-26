#!/usr/bin/env python
'''
Convert FASTA/FASTQ files

This will convert a FASTA or FASTQ file to the HPT version, removing
all homopolymers. For FASTA files, you can also produce an optional
homopolymer index (hpi) file that will allow you to convert HPT mapped
coordinates to native coordinates.

The HPT converted file will be written to stdout.
'''

import sys
import os
import argparse
import hpt

def convert_fastx(fname, index=None):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='hpt fastx', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="FASTA/FASTQ file to convert (may be gzipped)")
    parser.add_argument('-index', help="Output an HPI index for converting back to native coordinates")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        sys.stderr.write('File: %s not found!\n\n' % args.filename)
        sys.exit(1)

    if not hpt.fastx_autodetect(args.filename):
        sys.stderr.write('File: %s is not a FASTA/FASTQ file!\n\n' % args.filename)
        sys.exit(1)


    print args

    convert_fastx(args.filename, index=args.index)
