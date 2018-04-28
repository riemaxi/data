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

concept = load_concept( open(sys.argv[1]), sys.argv[2], sys.argv[3].split(',') )

uppers = set()
lowers = set()
for line in sys.stdin:
	data = line.strip().split('\t')

	m = set([int(s) for s in data[2].split(',')])
	lowers = lowers | lower(m, concept)
	uppers = uppers | upper(m, concept)


print( *sorted(list(uppers - lowers)), sep = '\n' )
