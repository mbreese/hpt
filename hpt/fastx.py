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
import gzip
import argparse
import hpt


def maxqual(quals):
    '''
    >>> maxqual('ACBD')
    'D'
    >>> maxqual(';;;;')
    ';'
    '''

    maxval = 0
    for q in quals:
        if ord(q) > maxval:
            maxval = ord(q)
    return chr(maxval)


def convert_fastq(fname, qualfunc='max'):
    for name, seq, qual in hpt.FASTQReader(fname):
        convseq = ''
        convqual = ''

        for pos, base, count, posquals in hpt.convert_seq(seq, qual):
            convseq += base
            if qualfunc == 'max':
                convqual += maxqual(posquals)

        sys.stdout.write('@%s\n%s\n+\n%s\n' % (name, convseq, convqual))


def convert_fasta(fname, index=None, wrap=50):
    lastname = None
    buf = ''
    last = (0, '', 0, '')
    idxfile = None

    if index:
        idxfile = gzip.open(index, 'w')

    for name, seq in hpt.FASTAChunkedReader(fname):
        if not seq:
            continue

        if name != lastname:
            if buf:
                buf += last[1]

                while len(buf) >= wrap:
                    sys.stdout.write('%s\n' % buf[:wrap])
                    buf = buf[wrap:]
                sys.stdout.write('%s\n' % buf)

            sys.stdout.write('>%s\n' % name)
            buf = ''
            pos = 0
            lastname = name
            last = (0, '', 0, '')

            if idxfile:
                idxfile.write('>%s\n' % name)

        hplist = list(hpt.convert_seq(seq, '', *last))
        last = hplist[-1]

        for pos, base, count, quals in hplist[:-1]:
            if idxfile and count > 1:
                idxfile.write('%s\t%s\t%s\n' % (pos, base, count))

            buf += base

        while len(buf) >= wrap:
            sys.stdout.write('%s\n' % buf[:wrap])
            buf = buf[wrap:]

    buf += last[1]
    while len(buf) >= wrap:
        sys.stdout.write('%s\n' % buf[:wrap])
        buf = buf[wrap:]
    sys.stdout.write('%s\n' % buf)

    if idxfile:
        if last[2] > 1:
            idxfile.write('%s\t%s\t%s\n' % (last[0], last[1], last[2]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='hpt fastx', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="FASTA/FASTQ file to convert (may be gzipped)")
    parser.add_argument('-index', help="Output an HPI index for converting back to native coordinates (FASTA only)")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        sys.stderr.write('File: %s not found!\n\n' % args.filename)
        sys.exit(1)

    filetype = hpt.fastx_autodetect(args.filename)

    if filetype == 'fasta':
        convert_fasta(args.filename, index=args.index)
    elif filetype == 'fastq':
        if args.index:
            sys.stderr.write('Invalid argument! Index output not supported with FASTQ files!\n\n')
            sys.exit(1)
        convert_fastq(args.filename)
    else:
        sys.stderr.write('File: %s is not a FASTA/FASTQ file!\n\n' % args.filename)
        sys.exit(1)
