#!/usr/bin/env python3

import sys
import cleanneedle as cn
import binning as b
import stairify as s
import random

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

def mutation(s):
	BASE = 'ACGT'
	return ''.join([BASE[(BASE.index(b) + random.randint(0,3)) % 4] for b in s if random.random() < .5])

path = '../../../data/hot/reference/actinidia_eriantha_0.flast'
outpath = 'report.sta'

start = 10000
size = 5000
zero = 'GT'
base = 100
order = 1
top = 40
maxscore = 0.5

sequence = open(path).read().strip()

total = 0
count = 0

with open(outpath, 'w') as report:
	for _ in range(10):

		mutant = mutation(sequence)


		for i in range(1,321):
			window_size_0 = 256
			window_size_1 =  window_size_0 + i

			al = cn.Aligner()
			s0 = s.transform(len(sequence), window_size_0, b.transform(sequence, zero), base, order)
			s1 = s.transform(len(sequence), window_size_1, b.transform(sequence, zero), base, order)

			m0 = s.transform(len(mutant), window_size_0, b.transform(mutant, zero), base, order)
			m1 = s.transform(len(mutant), window_size_1, b.transform(mutant, zero), base, order)

			d0,d1 = cn.Tool.distance(s0,m0), cn.Tool.distance(s1,m1)
			print(d0, window_size_0)
			print(d1, window_size_1)
			print(d1 > d0)
			report.write( '{:0.4f}\t{:0.4f}\t{}\t{}\t{}\n'.format(d0, d1,window_size_0, window_size_1, d1 > d0) )

			count += [0,1][d1 > d0]
			total += 1

	print('{:0.2f}%'.format((100 * count)/total ))
	report.write( 'sample: {}\t positive: {}\t{:0.2f}%'.format(total, count, (100 * count)/total ) )

