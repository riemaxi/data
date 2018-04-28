#!/usr/bin/env python3

import sys

def readarg(i, dv = ''):
	try:
		return sys.argv[i]
	except:
		return dv

def createmask(lst):
	a = [s.strip().split('-') for s in lst]

	a = [{int(s[0])} if len(s)<2 else set(range(int(s[0]), int(s[1]) + 1)) for s in a]

	mask = set()
	for s in a:
		mask = mask | s 

	return sorted(list(mask))

sep = sys.argv[1]
mask = createmask(readarg(2).split(','))

for line in sys.stdin:
	row = line.strip().split(sep)

	print('\t'.join([row[i] for i in mask]))
