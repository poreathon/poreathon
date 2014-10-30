poreathon
=========

Pipeline for poreathon

Getting started.

Dependencies

- bPipe
  http://download.bpipe.org/versions/bpipe-0.9.8.6_rc2.tar.gz

  (bPipe should be in PATH)

To run:

bpipe run -r -d output_dir -p ENTRYPOINT=recipes/recipe_name -p params.xml pipeline input/nanopore/ecoli_k12_mg1655/Ecoli_R73_2D.fasta

e.g. to run SPAdes assembly:

bpipe run -r -d output/nickloman-spades -p ENTRYPOINT=recipes/nickloman-spades.pipe @params.txt assembly.pipe input/nanopore/Ecoli_both_2D.fastq

bpipe run -r -f output/alignments/nickloman-last-q1/bpipe_report.html -d output/alignments/nickloman-last-q1 -p ENTRYPOINT=recipes/nickloman-last-q1.pipe @params.txt pipelines/alignment.pipe input/nanopore/Ecoli_R73_2D.fasta

Dependencies:

export PATH=$PATH:/mnt/phatso/nick/poreathon/bin/bpipe-0.9.8.6/bin:/mnt/phatso/nick/poreathon/bin/SPAdes-3.1.1-Linux/bin:/mnt/phatso/nick/poreathon/bin/last-490/src:/mnt/phatso/nick/poreathon/bin/last-490/scripts:/mnt/phatso/nick/poreathon/bin/samtools-1.1:/mnt/phatso/nick/poreathon/analysis:/mnt/phatso/nick/poreathon/bin/bwa-0.7.10

