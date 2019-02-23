#!/usr/bin/env python3

import dataset as ds
from parameter import p
import random

query = p.query
sample_size = int(p.sample_size)
min_size = int(p.min_size)
unit = int(p.window_size)//2
cutoff_factor = int(p.cutoff_factor)

records = ds.records(rs=4, input=open(query))
while sample_size > 0:
	r = next(records)[1]
	if random.random() <= .5:
		if len(r) >= min_size:
			cutoff = len(r) % unit
			print(cutoff_factor * cutoff, r, sep='\t')
			sample_size -= 1

