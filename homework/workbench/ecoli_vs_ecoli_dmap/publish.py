#!/usr/bin/env python3

import sys

path = 'heatmap.txt'

groups = 31
computations = 102
maxvalue = 100.0

print(groups, computations, maxvalue, 'init')
for line in open(path):
	row, col, score = line.strip().split()
	print(row,col,score)
