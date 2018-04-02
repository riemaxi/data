#!/usr/bin/env python3
import sys

#from https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm

#scoring schema
SCR_MATCH = 1
SCR_MISMATCH = -1
SCR_INDEL = -1

GAP = '-'

def match_score(a,b):
	return SCR_MATCH if a==b else SCR_MISMATCH

sequence = []
for line in sys.stdin:
	sequence.append(line.strip())


cols = len(sequence[0]) + 1
rows = len(sequence[1]) + 1

grid = [[0 for x in range(cols)] for y in range(rows) ]

for i in range(len(grid[0])):
	grid[0][i] = -i

for i in range(len(grid)):
	grid[i][0] = -i

#score aupdate - core of the algorithm
for r in range(1,len(sequence[1]) + 1):
	for c in range(1,len(sequence[0]) + 1):
		grid[r][c] = max( [grid[r-1][c-1] + match_score(sequence[1][r-1], sequence[0][c-1]), grid[r-1][c] + SCR_INDEL, grid[r][c-1] + SCR_INDEL] )

c = cols - 1
r = rows - 1

a = sequence[0][c-1]
b = sequence[1][r-1]

while r > 1:
	while c > 1:
		if grid[r-1][c-1] >= max(grid[r][c-1], grid[r-1][c]):
			a = sequence[0][c-2] + a
			b = sequence[1][r-2] + b
			r = r - 1
			c = c -1
		else:
			if grid[r-1][c] > max(grid[r-1][c-1], grid[r][c-1]):
				a = GAP + a

				b = sequence[1][r-2] + b
				r = r - 1
			else:
				a = sequence[0][c-2] + a

				b = GAP + b
				c = c - 1

print(a,b, sep = '\n')
