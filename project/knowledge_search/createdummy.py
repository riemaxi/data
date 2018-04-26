#!/usr/bin/env python3

import sys

def readarg(i, dv = ''):
	try:
		return sys.argv[i]
	except:
		return dv

rows = int(readarg(1, 100))
cols = int(readarg(2, 100))
sep = '\t'

for r in range(rows):
	for c in range(cols):
		print('d_{}_{}'.format(r,c), end = sep)
	print()
