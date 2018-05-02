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

classes = sys.argv[1]
sep =  sys.argv[2]
criteria =  sys.argv[3].split(',')

concept = load_concept( open(classes),sep,criteria )

for line in sys.stdin:
	data = line.strip().split('\t')

	s = subset(data[2].split(','), concept)
	if s:
		print( *list(s), sep='\n')

