#!/usr/bin/env python3

import dataset as ds
import math

def stdv(mean,n, lst):
	return math.sqrt( sum([(float(c)-mean)**2 for c in lst])/(n-1) )

def level(s,c,maxc, stdvc):
	return stdvc/(abs(maxc - c) + stdvc)

# Creates the header for the next step: filter
# The header is composed by three values separated by tabs: maximum, mean and standard deviation for the mapping size

path = 'report.map'
report = 'heatmap.txt'

lst = []
c = 0
maxc = float('-inf')
for line in open(path):
	rid, qid, cnt,  rs, re, qs,qe, score = line.strip().split('\t')
	cnt = int(cnt)
	maxc = max(maxc, cnt)
	c += cnt
	lst += [(rid, qid, cnt, float(score))]

# prints the header
n = len(lst)
stdvc = stdv(c/n,n,[f[2] for f in lst])

# prints the list
with open(report,'w') as file:
	for rid, qid, cnt , score in lst:
		if cnt>0:
			rec = '{}\t{}\t{:0.4f}'.format(rid, qid, 100 * (score/cnt) * level(score,cnt,maxc, stdvc))

			file.write(rec + '\n')
			print(rec)

