#!/usr/bin/env python3

import sys

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv

i = read_int_arg(1,1)

for line in sys.stdin:
	data = line.strip().split('\t')
	print(data[0], data[i], sep = '\t' )
