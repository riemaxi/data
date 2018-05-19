#!/usr/bin/env python3
import sys

def vector(s):
	v = {'A':0, 'C': 0, 'G': 0, 'T' : 0}
	for b in s:
		v[b] = v.get(b,0) + 1

	return v.values()

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv

def read_arg(i, dv):
	try:
		return sys.argv[i]
	except:
		return dv

l = read_int_arg(1,1000)
dest = read_arg(2,'stairified.tsv')

with open(dest, 'w') as f:
	for line in sys.stdin:
		seq = line.strip().upper()
		v = vector( seq )
		print( *v, sep = '\t' )
		f.write( '\t'.join( [str(n) for n in v] ) + '\n' )
