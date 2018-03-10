#!/usr/bin/env python3

import sys

def customize(h):
	print ( open(h).read().strip() )

customize('header.vcf')

for line in sys.stdin:
	print(line.strip())
