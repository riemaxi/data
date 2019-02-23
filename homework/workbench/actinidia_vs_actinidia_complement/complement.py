#!/usr/bin/env python3

import sys
import math
import dataset as ds
import binning as b
import stairify as s
from parameter import p

def distance(a,b,size):
        return math.sqrt(sum([(a[i]-b[i])**2 for i in range(size)]))

def equal(a,b, epsilon):
        return distance(a,b, len(a)) <= epsilon

wsize = int(p.window_size)
zero = p.zero
min_size = int(p.min_size)

margin = int(p.margin)
sample_size = int(p.sample_size)
epsilon = float(p.epsilon)

matches = 0
max_cutoff = 0
min_cutoff = int(p.window_size)//2
for r in ds.records():
	cutoff, data = r[0].split()
	cutoff = int(cutoff)
	if cutoff > 0:
		dlen, data = len(data[:-cutoff]), data[:-cutoff]
	else:
		dlen = len(data)


	acomp = s.transform(dlen, wsize, b.complement_transform(data, zero))
	bcomp = s.complement_transform(dlen, wsize, b.transform(data, zero))

	if margin > 0:
		acomp, bcomp = acomp[margin:-margin], bcomp[margin:-margin]

	eq = equal(acomp, bcomp, epsilon)
	matches += [0,1][eq]
	max_cutoff = max(max_cutoff, cutoff)
	min_cutoff = min(min_cutoff, cutoff)

	print(eq, dlen, cutoff,  sep='\t')

print('matches(%) : {:.2f}\tmax cutoff : {}\tmin cutoff : {}'.format( (matches * 100)/sample_size , max_cutoff, min_cutoff))

