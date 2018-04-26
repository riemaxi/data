#!/usr/bin/env python3

import sys

def readarg(i, dv = ''):
	try:
		return sys.argv[i]
	except:
		return dv

def createmask(lst):
	mask = [s.strip().split(':') for s in lst]

	mask = [(a.split('-'),b) for a,b in mask]

	mask = [((int(a[0]),int(a[0])+1),b) if len(a)==1 else ((int(a[0]),int(a[1])),b) for a,b in mask]

	return mask

mask = createmask(sys.argv[1:])
print(mask)

'''
for line in sys.stdin:
	print(line.strip())

'''
