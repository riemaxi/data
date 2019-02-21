#!/usr/bin/env python3

import sys
import clearwater as cw

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
count = int(sys.argv[4])

mapper = cw.Warmmapper()

with open(report,'w', buffering = 1) as file:
	for line in open(reference):
		ri, r = line.strip().split('\t')

		for line in open(query):
			qi, q = line.strip().split('\t')

			print('mapping ...', ri, qi, len(r), len(q), sep = '\t')

			count -= 1

			if not count:
				break
		if not count:
			break
