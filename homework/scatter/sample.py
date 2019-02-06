#!/usr/bin/env python3

import os
import random
import dataset as ds
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

def max_query_size(records):
	max_size = 0
	for r in records:
		max_size = max(max_size, len(r[1]))
	return max_size

def mutation(seq, n):
	BASE = 'ACGT'
	return ''.join([(b, BASE[(BASE.index(b) + random.randint(1,3)) % 4])[ random.choices([False,True], [(100-n)/100, n/100])[0] ] for b in seq])

def mutations(id, seq, step = 25):
	for i in range(0, 100 + step, step):
		yield id, i, mutation(seq,i)

def similarity(a,b):
	return (100 * sum([[0,1][a[i] == b[i]] for i in range(len(a))]))/len(a)


open('process.pid','a').write('{}\n'.format(os.getpid()))

unit = int(p.window_size)//2
margin = int(p.margin)
min_size = int(p.min_size)

cutoff_factor = int(p.cutoff_factor)
query = p.query

records = ds.records(rs=4, input=open(query), ok = lambda r: len(r[1]) >= min_size)

# sample reference fragment mutations
reference = p.reference
fragment_size = 5 * max_query_size(records)

for id, fragment in fragments(reference, cutoff_factor, unit, margin, fragment_size):
	for id,i, m in mutations(id, fragment):
		print('control {}_{}'.format(id,i), m, sep='\t')


# sample queries
sample_size = int(p.sample_size)
print_sample = [print_without_cutoff, print_with_cutoff][cutoff_factor]

records = ds.records(rs=4, input=open(query), ok = lambda r: len(r[1]) >= min_size)
while sample_size > 0:
	r = next(records)
	id, data = r[0].split()[0], r[1]

	print_sample(id, data, cutoff_factor, unit, margin)

	sample_size -= 1

