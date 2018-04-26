#!/usr/bin/env python3

import sys

def readarg(i, dv = ''):
	try:
		return sys.argv[i]
	except:
		return dv


def createmask(lst):
	lst = [s.strip().split(':') for s in lst]
	lst = [(int(a),b.split('-')) for a,b in lst]
	mask = {}
	for a,b in lst:
		mask[a] = (int(b[0]),int(b[0])+1) if len(b)==1 else (int(b[0]),int(b[1])+1)

	return mask

def match(row, mask):
	for i,c in mask:
		if int(row[i]) in range(c[0],c[1]):
			return False
	return True


mask = createmask(sys.argv[1:]).items()
sep = '\t'
for line in sys.stdin:
	row = line.strip().split(sep)

	if match(row, mask):
		print(*row, sep = '\t')


