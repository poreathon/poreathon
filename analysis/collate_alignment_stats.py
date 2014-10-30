import glob
import os
import yaml
import sys
import pysam
from collections import Counter
from Bio import SeqIO
import numpy

def count_sequences(input_file, typ):
	return len([s for s in SeqIO.parse(open(input_file), typ)])

def dump_pipeline(input_file, recipe_name, recipe_info):
	input_lines = count_sequences("input/nanopore/%s.%s" % (input_file, recipe_info['input']), recipe_info['input'])

	## this is all super hacky right now and will break eventually
	filenames = glob.glob("output/alignment/%s/%s.*.bam" % (recipe_name, input_file))
        unaligned = 0
        best_align = {}
        bam = pysam.Samfile(filenames[0])
        for read in bam:
                if read.is_unmapped:
                        unaligned += 1
                        continue

                if read.qname not in best_align:
                        best_align[read.qname] = read.alen

        output = recipe_info
	output['Recipe'] = recipe_name
	output['Input'] = input_file
        output['Mean_Alignment_Length'] = int(numpy.mean(best_align.values()))
	output['Aligned_Reads'] = len(best_align.values())
	output['Unaligned_Reads'] = input_lines - output['Aligned_Reads']
	output['Percent_Aligned'] = "%.2f" % (100.0 / input_lines * output['Aligned_Reads'])

	print "- " + yaml.dump(output)

	filenames = glob.glob("output/alignment/%s/%s*.draw_histo.png" % (recipe_name, input_file))
	os.system("cp %s ../poreathon.github.io/output/alignment/%s_%s.histogram.png" % (filenames[0], recipe_name, input_file))


pipelines = yaml.load(file('pipelines.yaml'))
recipes = glob.glob('recipes/*.yaml')
recipes = dict([(r[8:-5], yaml.load(file(r))) for r in recipes])

for input_file in pipelines['alignment']:
	for recipe_name, recipe_info in recipes.iteritems():
		if recipe_info['type'] == 'alignment':
			dump_pipeline(input_file, recipe_name, recipe_info)
