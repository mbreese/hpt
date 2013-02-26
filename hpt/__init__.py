import os
import gzip

from eta import ETA


def gzip_aware_reader(fname):
    if fname[-3:] == '.gz':
        f = gzip.open(fname)
    else:
        f = open(fname)

    eta = ETA(os.stat(fname).st_size, fileobj=f)
    for line in f:
        yield line

    f.close()
    eta.done()


def fastx_autodetect(fname):
    line = gzip_aware_reader(fname).next()
    if line[0] == '>':
        return 'fasta'
    elif line[0] == '@':
        return 'fastq'
    return ''


def FASTAChunkedReader(fname):
    name = ''

    for line in gzip_aware_reader(fname):
        if line[0] == '>':
            name = line.strip()[1:]
        else:
            yield (name, line.strip().upper())


def FASTQReader(fname):
    reader = gzip_aware_reader(fname)

    while True:
        try:
            name = reader.next().strip().upper()
            seq = reader.next().strip()
            reader.next()
            qual = reader.next().strip()

            yield (name, seq, qual)
        except:
            break


def convert_seq(seq, qual='', lastpos=0, lastbase='', lastcount=0, lastquals=''):
    '''
    Strip out hp runs
    >>> list(convert_seq('aatggc'))
    [(0, 'a', 2, ''), (2, 't', 1, ''), (3, 'g', 2, ''), (5, 'c', 1, '')]

    Overlap base is different
    seq: aatggc/aatggc
    >>> list(convert_seq('aatggc', '', 5, 'c', 1))
    [(5, 'c', 1, ''), (6, 'a', 2, ''), (8, 't', 1, ''), (9, 'g', 2, ''), (11, 'c', 1, '')]

    Overlap base is same
    seq: aatggc/ccaatg/gggatt
    >>> list(convert_seq('ccaatg', '', 5, 'c', 1))
    [(5, 'c', 3, ''), (8, 'a', 2, ''), (10, 't', 1, ''), (11, 'g', 1, '')]
    >>> list(convert_seq('gggatt', '', 11, 'g', 1))
    [(11, 'g', 4, ''), (15, 'a', 1, ''), (16, 't', 2, '')]
    '''

    startpos = lastpos

    if lastpos:
        lastpos += lastcount

    if not qual:
        qual = ' ' * len(seq)

    for s, q in zip(seq, qual):
        if s == lastbase:
            lastcount += 1
            if q != ' ':
                lastquals += q
        else:
            if lastbase:
                yield (startpos, lastbase, lastcount, lastquals)

            lastbase = s
            lastcount = 1
            startpos = lastpos
            if q != ' ':
                lastquals = q

        lastpos += 1

    yield (startpos, lastbase, lastcount, lastquals)
