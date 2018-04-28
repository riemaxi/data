#!/usr/bin/env python3

import sys

def load_concept(f,sep, criteria):
	data = [s.split(sep) for s in f.read().strip().split('\n')]
	l = [int(s[0]) for s in data if s[-1] in criteria] 

	return set(l)

def subset(m,c):
	s = set([int(i) for i in m])
	if s <= c:
		return s
	else:
		return None

concept = load_concept( open(sys.argv[1]), sys.argv[2], sys.argv[3].split(',') )

for line in sys.stdin:
	data = line.strip().split('\t')

	s = subset(data[2].split(','), concept)
	if s:
		print( *list(s), sep='\n')

