#!/usr/bin/env python3
import sys
import os
import time

import clearwater as cw
from parameter import p

def tofloat( data):
	return [float(f) for f in data]


def reference_fragments():
	for line in open(p.hot_reference):
		id,f = line.strip().split('\t')
		yield id, tofloat(f.split(' '))


def lookup_and_report(qid, qdata):
	count = 0
	for rid, rdata in reference_fragments():
		starttime = time.time()
		(scr,(rstart,rend),(qstart,qend), cnt),_ = cw.Warmmapper().map(rdata, qdata)
		elapsed = time.time() - starttime

		screport = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(rid, qid, cnt, rstart, rend, qstart, qend, '{:0.2f}\t{:0.5f}'.format(scr, elapsed))

		print(screport)

		count += 1
	return count

count = 0
for line in sys.stdin:
	id, data = line.strip().split('\t')
	size = lookup_and_report(id, tofloat(data.split(' ')))

	count += size



