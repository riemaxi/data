#!/usr/bin/env python3

import sys

def load_concept(f,sep, criteria):
	data = [s.split(sep) for s in f.read().strip().split('\n')]
	l = [int(s[0]) for s in data if s[-1] in criteria] 

	return set(l)

def upper(m,c):
	return m & c

def lower(m,c):
	return m & c if m <= c else set()

def boundary(m,c):
	return upper(m,c) ^ lower(m,c)

concept = load_concept( open(sys.argv[1]), sys.argv[2], sys.argv[3].split(',') )

for line in sys.stdin:
	data = line.strip().split('\t')

	m = set([int(s) for s in data[2].split(',')])
	s = boundary(m,concept)	
	if s:
		print(*list(s), sep='\n')
