import sys
import pysam
from collections import Counter
import numpy

def stats(fn):
	unaligned = 0
	best_align = {}
	bam = pysam.Samfile(fn)
	for read in bam:
		if read.is_unmapped:
			unaligned += 1
			continue

		if read.qname not in best_align:
			best_align[read.qname] = read.alen

	print """- Filename: %s
  Mean_Alignment_Length: %d
  Unaligned_Reads: %d
  Aligned_Reads: %d""" % (fn, numpy.mean(best_align.values()), unaligned, len(best_align.values()))

for fn in sys.argv[1:]:
	stats(fn)

