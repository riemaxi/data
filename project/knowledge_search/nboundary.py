#!/usr/bin/env python3

import sys

sep = sys.argv[1]
arity = int(sys.argv[2])

boundary = [(float('+inf'), float('-inf')) for i in range(arity)]

for line in sys.stdin:
	v = [float(s) for s in line.strip().split(sep)]

	boundary = [(min(v[i], boundary[i][0]), max(v[i],boundary[i][1])) for i in range(len(v))]

print('\n'.join(['{}\t{}'.format(a,b) for a,b in boundary]))
