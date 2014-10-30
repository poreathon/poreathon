# Proposed Pipelines

## Alignment

The alignment pipeline aligns FASTA or FASTQ or FAST5 files to a reference.

Input: FASTA/FASTQ/FAST5 file & reference
Output: Sorted BAM file

Tests:
 - # mapped/ # unmapped
 - median/mean coverage
 - time to run
 - histogram of alignment lengths
 - coverage plots

## Alignment corrector

This pipeline takes an alignment and post-processes it, e.g. with the aim of improving SNP or indel calling sensitivity/specificity.

Input: Sorted BAM file
Output: Sorted BAM file

Tests:
 - ??

## Consensus calling (normal reference)

This pipeline takes results from alignment or alignment corrector and produces a consensus output.

Input: FASTA file & reference
Output: VCF file

Tests:
  - number of bases correct
  - number of bases called
  - number of bases incorrect (SNPs, indels)
 
## Consensus calling (mutated references)

The reference is mutated, e.g. 0.1%, 1%, 5% nucleotide divergence and a consensus is produced.

Tests:
  - truth table
  - ROC curves
   
## Hybrid assembly

De novo assembly using Illumina reads as guide.

Tests:
  - QUAST output

## Nanopore-only assembly

Nanopore only assembly.

## Read correction by Illumina

Reads are corrected by Illumian reads.

## Read correction de novo

Reads are corrected, e.g. by a statistical model or by FAST5 squiggles.


