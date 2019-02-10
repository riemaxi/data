#!/usr/bin/env python3

import os
import sys
import random
import dataset as ds
import stairify as s
import binning as b
from parameter import p

def print_with_cutoff(id, data, cutoff_factor, unit, margin):
	cutoff = cutoff_factor * (len(data) % unit)
	print(id, data[:-cutoff] if cutoff else data, sep='\t')

def print_without_cutoff(id, data,cutoff_factor, unit, margin):
	print(id, data[margin:-margin] if margin else data, sep='\t')


def fragments(reference, cutoff_factor, unit, margin, fragment_size):
	data = open(reference).read().strip()
	cutoff = cutoff_factor * (len(data) % unit)
	if cutoff:
		data = data[:-cutoff]
	elif margin:
		data = data[margin:-margin]

	for i in range(0, len(data), fragment_size//2):
		yield i, data[i:i + fragment_size]


def stairify(seq, window_size, zero, precision):
	seq = s.transform(len(seq), window_size, b.transform(seq, zero))
	template = '{:.PRECISIONf}'.replace('PRECISION', precision)
	return ' '.join([template.format(f) for f in seq])

unit = int(p.window_size)//2
margin = int(p.sample_margin)
min_size = int(p.sample_min_size)

cutoff_factor = int(p.sample_cutoff_factor)
query = p.query

records = ds.records(rs=4, input=open(query), ok = lambda r: len(r[1]) >= min_size)

mqsize = int(sys.argv[1])
fragment_size = 3 * mqsize

zero = p.zero
window_size = int(p.window_size)
precision = p.precision

# create hot reference
reference = p.reference
hot_reference = p.hot_reference

if not os.path.isfile(hot_reference):
	with open(hot_reference,'w') as file:
		for id, fragment in fragments(reference, cutoff_factor, unit, margin, fragment_size):
			file.write('{}\t{}\n'.format(id, stairify(fragment, window_size, zero, precision)))


# sample queries
sample_size = int(p.sample_size)

records = ds.records(rs=4, input=open(query), ok = lambda r: len(r[1]) >= min_size)
print_sample = [print_without_cutoff, print_with_cutoff][cutoff_factor]

id = 0
while sample_size > 0:
	r = next(records)
	_, data = r[0].split()[0], r[1]

	if random.random() > .5:
		print_sample(id, data, cutoff_factor, unit, margin)

		sample_size -= 1
		id += 1

