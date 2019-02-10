#!/usr/bin/env python3

import os
import dataset as ds
from parameter import p

def max_query_size():
	max_size = 0
	for r in ds.records(open(p.query), rs=4):
		max_size = max(max_size, len(r[1]))
	return max_size

mqsize = max_query_size()

os.system('./sample.py {0} | ./scatter.py {0}| ./lookup.py | ./organize.py'.format(mqsize))

