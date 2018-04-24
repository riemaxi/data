#!/usr/bin/env python3

import sys

def compare(a,b, attr):
	key = '_'.join([ a[attr[i]] for i in range(len(attr))])
	return key, [a[attr[i]] == b[attr[i]] for i in range(len(attr))].count(False) == 0

sep = ','
attr = [int(s) for s in sys.argv[1].split(',')]

last = None
eclass = {}
for line in sys.stdin:
	a,b = line.strip().split('\t')

	a = a.split(sep)
	b = b.split(sep)
	key, equals = compare(a, b, attr)
	if equals:
		print(key, a[0], b[0], sep = '\t')
