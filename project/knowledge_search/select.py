#!/usr/bin/env python3

import sys

from selectcriteria import match

sep = sys.argv[1]
for line in sys.stdin:
	data = line.strip().split(sep)
	if match(data):
		print('\t'.join(data))
