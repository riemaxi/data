#!/usr/bin/env python3

import sys

print('data = [')
for line in sys.stdin:
	row = line.strip().split('\t')
	print('"{}",'.format('\t'.join(row)))

print(']')
