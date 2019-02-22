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

sequence = open(path).read().strip()
inversion = sequence[:start] + sequence[start + size:]

al = cn.Aligner()
ss = s.transform(len(sequence), window_size, b.transform(sequence, zero))
si = s.transform(len(inversion), window_size, b.transform(inversion, zero))

with open(outpath, 'w') as file:
	for dr, dq, score in cn.Tool.topalignments(al.deployments(ss, si, first = False), maxscore = 0.0, top = 10):
		file.write( '{}\n{}\n'.format( dr, dq ) )
		print('ss', 'si', score , flush = True, sep='\t')
