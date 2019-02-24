#!/usr/bin/env python3

import dataset as ds
import os

path = 'report.aln'
outpath = 'align.txt'
minscore = 0.36

with open(outpath + '.random','w') as file:
	for r in ds.records(input=open(path), rs=5):
		if float(r[3]) >= minscore:
			file.write('{}\t{}\t{}\n'.format(r[3], r[1], r[2]))
