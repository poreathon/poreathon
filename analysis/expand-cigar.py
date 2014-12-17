#!/usr/bin/python

# from the legendary arq5x

import sys
import pysam
import argparse
from itertools import groupby

# http://pysam.readthedocs.org/en/latest/api.html#pysam.AlignedRead.cigar
MATCH  = 0  # M
INS    = 1  # I
DEL    = 2  # D
SKIP   = 3  # N
SOFT   = 4  # S
HARD   = 5  # H
PAD    = 6  # P
EQUAL  = 7  # =
DIFF   = 8  # X


def get_chrom(fasta_fh, chrom):
    """
    Return the chromosome sequence
    """
    return fasta_fh.fetch(chrom)

def expand_match_op(qry_seq, ref_seq):
    """
    Return an expanded list of CIGAR ops
    based upon nuceltotide matches (=, or 7)
    and mismatches (X, or 8)

    This onvert runs into RLE tuples (i.e. CIGAR ops/lengths)
    for example, the following:
    ref: ATTCAGGG
    qry: ATTCAGAG
    becomes (via _runs()):
         ======X=
    or:  77777787    
    this is converted to:
    [(7, 5), (8, 1), (7, 1)]
    """
    def _runs(qry_seq, ref_seq):
        """
        Create runs of matches and mismatches
        """
        for idx, q_nucl in enumerate(qry_seq):
            if q_nucl == ref_seq[idx]:
                yield 7 #EQUAL (=)
            else:
                yield 8 #DIFF (X)

    cigar_ops = []
    for k, v in groupby(_runs(qry_seq, ref_seq), lambda x: x):
        cigar_ops.append((k,len(list(v))))
    return cigar_ops

def main(args):

    bam = pysam.AlignmentFile(args.bam)
    fa = pysam.FastaFile(args.fasta)
    outfile = pysam.AlignmentFile("-", "wb", template=bam)

    prev_chrom_id = None
    curr_chrom_id = None
    curr_chrom_seq = None
    for read in bam:
        curr_chrom_id = read.reference_id

        # load the current chromosome into memory
        if curr_chrom_id != prev_chrom_id:
            curr_chrom_seq = get_chrom(fa, bam.getrname(curr_chrom_id))

        # iterate through the existing CIGAR
        # and replace M ops with expanded X and = ops.
        ref_pos = read.reference_start
        qry_pos = 0
        new_cigar = []
        for cigar_tuple in read.cigar:
            op = cigar_tuple[0]
            op_len = cigar_tuple[1]
            if op == EQUAL or op == DIFF or op == MATCH:
                if op == MATCH:
                    qry_seq = read.query_sequence[qry_pos:qry_pos+op_len]
                    ref_seq = curr_chrom_seq[ref_pos:ref_pos+op_len]
                    
                    # expand the M CIGAR op.
                    new_cigar_ops = expand_match_op(qry_seq, ref_seq)
                    for new_cigar_tuple in new_cigar_ops:
                        new_cigar.append(new_cigar_tuple)
                else:
                    new_cigar.append(cigar_tuple)
                ref_pos += op_len
                qry_pos += op_len
            elif op == DEL or op == SKIP:
                ref_pos += op_len
                new_cigar.append(cigar_tuple)
            elif op == INS or op == SOFT:
                qry_pos += op_len
                new_cigar.append(cigar_tuple)
            elif op == HARD:
                new_cigar.append(cigar_tuple)

        # replace the old CIGAR and write updated record.
        read.cigar = new_cigar
        outfile.write(read)
        prev_chrom_id = curr_chrom_id

    outfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='expand_cigar.py')
    parser.add_argument('--bam',
    dest='bam',
    metavar='STRING',
    help='The sorted BAM file whose CIGARs you wish expand.')
    parser.add_argument('--fasta',
    dest='fasta',
    metavar='STRING',
    help='The reference genome used to create the BAM.')
    # parse the args and call the selected function
    args = parser.parse_args()
    
    main(args)

