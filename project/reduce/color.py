#!/usr/bin/env python3

import sys

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv


def color(data, base = 4):
	v = [int(data[i]) * base**i for i in range(len(data))]
	return sum(v)

base = read_int_arg(1,4)

for line in sys.stdin:
	data = line.strip().split('\t')
	print(data[0], color(data[1:], base), sep = '\t' )
