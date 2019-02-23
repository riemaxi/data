#!/usr/bin/env python3

import sys

path = 'heatmap.txt'

groups = 9
computations = 102

print(groups, computations,'init')
for line in open(path):
	row, col, score = line.strip().split()
	print(row,col,score)
