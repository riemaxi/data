#!/usr/bin/env python3

import sys
import dataset as ds
import binning as b
import stairify as s
from parameter import p

def stairify(data, window_size, zero, order = 0, base = 100):
	return s.transform(len(data), window_size, b.transform(data, zero), base, order)

def stair2str(data, template):
	return ' '.join([template.format(f) for f in data])

def reference_mutation(idx, path, size):
	i = 0
	for line in open(path):
		id, data = line.strip().split('\t')
		if i == idx:
			return ' '.join(data.split(' ')[:size])
		i += 1

window_size = int(p.window_size)
zero = p.zero
order = int(p.derivative_order)
template = '{:.PRECISIONf}'.replace('PRECISION',p.precision)

mqsize = 2 * int(sys.argv[1])//int(p.window_size)

for r in ds.records():
	id, data = r[0].split('\t')

	if id in ['3','7','17']:
		print(id, reference_mutation(int(id),p.hot_reference, mqsize), sep = '\t')
	else:
		print(id, stair2str(stairify(data, window_size, zero, order), template), sep = '\t')

