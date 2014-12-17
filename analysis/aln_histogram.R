#!/usr/bin/Rscript
library(ggplot2)
args=commandArgs(TRUE)
cov=read.table(args[1], sep="\t", header=T, stringsAsFactors=T)
cov=subset(cov, align_len != 'None')
cov=cbind(cov,"frac" = as.numeric(cov$align_len) / as.numeric(cov$read_len))
p=ggplot(cov, aes(x=frac)) + geom_histogram() + xlim(0, 2) + theme_bw()
ggsave(filename=args[2], plot=p)
