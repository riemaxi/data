#!/usr/bin/env python3

import sys

def load_concept(f,sep, criteria):
	data = [s.split(sep) for s in f.read().strip().split('\n')]
	l = [int(s[0]) for s in data if s[-1] in criteria] 

	return set(l)

def intersect(m,c):
	m =  set([int(i) for i in m])
	return m & c

concept = load_concept( open(sys.argv[1]), sys.argv[2], sys.argv[3].split(',') )

for line in sys.stdin:
	data = line.strip().split('\t')

	s = intersect(data[2].split(','), concept)
	if s:
		print( *list(s), sep='\n')

