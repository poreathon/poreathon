#!/usr/bin/Rscript
library(ggplot2)
args=commandArgs(TRUE)
cov=read.table(args[1], sep="\t", header=F)
p=ggplot(cov, aes(x=V2, y=V3)) + geom_bar(stat="identity") + scale_x_continuous("Coverage depth") + scale_y_continuous("Number of bases") + theme_bw()
ggsave(filename=args[2], plot=p)
