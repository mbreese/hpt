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


def FASTAReader(fname):
    name = ''
    seq = ''

    for line in gzip_aware_reader(fname):
        if line[0] == '>':
            if name and seq:
                yield (name, seq)
            name = line.strip()[1:]
            seq = ''
        else:
            seq += line.strip()


def FASTQReader(fname):
    reader = gzip_aware_reader(fname)

    while True:
        try:
            name = reader.next().strip()
            seq = reader.next().strip()
            reader.next()
            qual = reader.next().strip()

            yield (name, seq, qual)
        except:
            break
