#!/usr/bin/env python3

import sys
import cleanneedle as cn

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
count = int(sys.argv[4])

with open(report,'w', buffering = 1) as file:
	al = cn.Aligner()
	for line in open(reference):
		ri, r = line.strip().split('\t')

		for line in open(query):
			qi, q = line.strip().split('\t')

			print('aligning ...', ri, qi, len(r), len(q), sep = '\t')

			for dr, dq, score in cn.Tool.topalignments(al.deployments(string2stairs(r), string2stairs(q))):

				file.write( '{}\t{}\n{}\n{}\n\n'.format( ri,qi, dr, dq, '{:0.2f}'.format(score) ) )

				print(ri, qi, '{:0.2f}'.format(score) , flush = True, sep='\t')

				count -= 1

				if not count:
					break
		if not count:
			break
