#!/usr/bin/env python3

import sys

DEFAULT_SIZE = 1000

def print_record(i):
	print('K',i*20, '\t'.join(['{}{}'.format(i,j) for j in range(0,17)]), sep = '\t')


try:
	size = int(sys.argv[1])
except:
	size = DEFAULT_SIZE

print( open('header.vcf').read().strip() )

[print_record(i)  for i in range(size)]
