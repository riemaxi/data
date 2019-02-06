#!/usr/bin/env python3

import sys
import os
import binning as b
import stairify as s
import dataset as ds
from parameter import p

def stair2str(data):
	return ' '.join(['{:0.2f}'.format(f) for f in data])

min_size = int(p.min_query_size)
zero = p.zero
window_size = int(p.window_size)
query = p.query

long_max_size = -1
short_max_size = -1
count = 0
long_count = 0

lpath = '{}/L_SIZE_MAXS_{}.fastq'.format(query, sys.argv[1])
spath = '{}/S_SIZE_MAXS_{}.fastq'.format(query, sys.argv[1])

with open(lpath,'w') as longs, open(spath,'w') as shorts:
	for r in ds.records(rs=4):
		size = len(r[1])
		stairdata = s.transform(size, window_size, b.transform(r[1], zero))

		if size >= min_size:
			longs.write('{}\t{}\n'.format(r[0], stair2str(stairdata)))

			long_count += 1
			long_max_size = max(len(stairdata), long_max_size)
		else:
			shorts.write('{}\t{}\n'.format(r[0], stair2str(stairdata)))
			short_max_size = max(len(stairdata), short_max_size)


		print(size, r[1][:30], sep='\t')

		count += 1


os.rename(lpath, lpath.replace('SIZE', str(count)).replace('MAXS',str(long_max_size)))
os.rename(spath, spath.replace('SIZE', str(count - long_count)).replace('MAXS',str(short_max_size)))

