#!/usr/bin/env python3

import os
import stairify as s
import binning as b

# parameter{
zero = 'GT'
window_size = 512
order = 1

reference = '../../../data/stage/reference/ecoli.fasta'

hot_reference = '../../../data/hot/reference/ecoli_0.flast'
hot_reference_stairs = '../../../data/hot/reference/ecoli_0_d.stairs'
hr_fsize = 24000

hot_query = hot_reference
hot_query_stairs = '../../../data/hot/reference/ecoli_0_dquery.stairs'
hq_fsize = 8000

report = 'report.map'

computations = 100

# }


def stairs2string(v, template = '{:0.2f}', sep=' '):
	return sep.join([template.format(f) for f in v])

def fragments(seq, size):
	step = size // 2
	for i in range(0, len(seq), step):
		yield i, seq[i:i + size]


def stairify(seq, zero, window_size, order = 1):
	return stairs2string(s.transform(len(seq), window_size, b.transform(seq, zero), order = order))

# flatten
os.system('./fasta_split.py {} ../../../data/hot/reference ecoli_'.format(reference))

# stairify
if not os.path.isfile(hot_query_stairs):
	with open(hot_query_stairs,'w') as file:
		for i, f in fragments( open(hot_query).read().strip(), hq_fsize ):
			file.write('{}\t{}\n'.format(i, stairify(f, zero, window_size, order) ))
			print(i, f[:20])

if not os.path.isfile(hot_reference_stairs):
	with open(hot_reference_stairs,'w') as file:
		for i, f in fragments( open(hot_reference).read().strip(), hr_fsize ):
			file.write('{}\t{}\n'.format(i, stairify(f, zero, window_size) ))
			print(i, f[:20])

# alignment
os.system('./map.py {} {} {} {}'.format(hot_reference_stairs, hot_query_stairs, report, computations))
