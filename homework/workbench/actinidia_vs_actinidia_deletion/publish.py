#!/usr/bin/env python3

import dataset as ds
import os

path = 'report.aln'
outpath = 'align.txt'
minscore = 0.3

with open(outpath + '.random','w') as file:
	for r in ds.records(input=open(path), rs=3):
		if float(r[2]) >= minscore:
			file.write('{}\t{}\t{}\n'.format(r[2], r[0], r[1]))
