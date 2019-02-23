#!/usr/bin/env python3

import sys
import cleanneedle as cn
import binning as b
import stairify as s

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

path = '../../../data/hot/reference/actinidia_eriantha_0.flast'
outpath = 'report.aln'

start = 10000
size = 5000
zero = 'GT'
window_size = 512
base = 100
order = 1
top = 100
maxscore = 0.2

sequence = open(path).read().strip()
inversion = sequence[:start] + sequence[start + size:]

al = cn.Aligner()
ss = s.transform(len(sequence), window_size, b.transform(sequence, zero), base, order)
si = s.transform(len(inversion), window_size, b.transform(inversion, zero), base, order)

with open(outpath, 'w') as file:
	for dr, dq, score in cn.Tool.topalignments(al.deployments(ss, si, first = False), maxscore, top):
		file.write( '{}\n{}\n{:0.8f}\n'.format( dr, dq, score ) )
		print('ss', 'si', score , flush = True, sep='\t')

