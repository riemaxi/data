#!/usr/bin/env python3

import sys

def intersect(x, repo):
	x = set([int(s) for s in x.split(',')])
	res = set()
	for y in repo:
		y = set([int(s) for s in y.split(',')])
		if x<=y or y<x:
			res |= (x & y)

	return x, res

repo = set()
for line in sys.stdin:
	a = line.strip()
#	print('--')
#	print(a)

	x, i = intersect(a, repo)
#	print(i)
	if not i:
		i = set([int(s) for s in a.split(',')])


#	print(repo)
	si = ','.join([str(n) for n in sorted(list(i))])
	if not si in repo:
		print(si)

	repo |= {si}
