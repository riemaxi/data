#!/usr/bin/env python3

import sys

for line in sys.stdin:
	id, data = line.strip().split('\t')
	print(id, len(data), data, sep='\t')
