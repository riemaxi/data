#!/usr/bin/env python3

import os
import stairify as s
import binning as b

# parameter{
zero = 'GT'
window_size = 512
reference = '../../../data/stage/reference/actinidia_eriantha.fasta'
query = '../../../data/stage/query/actinidia_eriantha.fastq'

hot_query = '../../../data/hot/query/actinidia_eriantha.flast'
hot_query_stairs = '../../../data/hot/query/actinidia_eriantha.stairs'

hot_reference = '../../../data/hot/reference/actinidia_eriantha_0.flast'
hot_reference_stairs = '../../../data/hot/reference/actinidia_eriantha_0.stairs'
hr_fsize = 40000

report = 'report.aln'

computations = 400

# }


def stairs2string(v, template = '{:0.2f}', sep=' '):
	return sep.join([template.format(f) for f in v])

def fragments(seq, size):
	step = size // 2
	for i in range(0, len(seq), step):
		yield i, seq[i:i + size]


def string2stairs(s):
	return [float(f) for f in s]

def stairify(seq, zero, window_size):
	return stairs2string(s.transform(len(seq), window_size, b.transform(seq, zero)))

# flatten
os.system('./fasta_split.py {} ../../../data/hot/reference actinidia_eriantha_'.format(reference))
os.system('./fastq_flatten.py {} ../../../data/hot/query actinidia_eriantha'.format(query))

# stairify
if not os.path.isfile(hot_query_stairs):
	with open(hot_query_stairs,'w') as file:
		for line in open(hot_query):
			id, data = line.strip().split('\t')
			file.write('{}\t{}\n'.format(id, stairify(data, zero, window_size) ))
			print(id, data[:100], len(data))

if not os.path.isfile(hot_reference_stairs):
	with open(hot_reference_stairs,'w') as file:
		for i, f in fragments( open(hot_reference).read().strip(), hr_fsize ):
			file.write('{}\t{}\n'.format(i, stairify(f, zero, window_size) ))
			print(i, f[:100])

# alignment
os.system('./align.py {} {} {} {}'.format(hot_reference_stairs, hot_query_stairs, report, computations))
