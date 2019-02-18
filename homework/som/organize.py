#!/usr/bin/env python3

import sys
import math
from parameter import p

def stdv(mean,n, lst, field = 3):
	return math.sqrt( sum([(float(r[field])-mean)**2 for r in lst])/(n-1) )

def statistics():
	totalcnt = 1
	maxcnt = float('-inf')
	lst = []
	for line in sys.stdin:
		rid, qid,cnt, rstart, rend, qstart,qend, score,_ = line.strip().split('\t')

		totalcnt += int(cnt)
		maxcnt = max(maxcnt, int(cnt))
		lst += [(rid, qid, cnt, rstart, rend, qstart, qend, score)]

		print(rid, qid, cnt, sep='\t')

	n = len(lst)
	if n>1:
		return n, maxcnt, totalcnt/n, stdv(totalcnt/n, n, lst), lst
	else:
		return 0, 0,0,0, []


def level(cnt,maxcnt, stdvc):
	return stdvc/(abs(maxcnt - cnt) + stdvc)


def filter(n, maxcnt, stdv, lst, threshold = 0.3):
	for rid, qid, cnt, rstart, rend, qstart, qend, score in lst:
		cnt = int(cnt)
		score = float(score)
		if cnt>0:
			score = (score/cnt) * level(cnt, maxcnt, stdv)
			if score >= threshold:
				yield rid, qid, str(cnt), rstart, rend, qstart, qend, str(score)

def print_post(data, file):
	file.write('{}\n'.format(data))

def post_init(sample_size, repo):
	data = '{}\t{}'.format(sample_size, ','.join(reference_fragment_index(p.hot_reference)))
	print_post(data, repo)

def report(threshold, repo):
	n,maxcnt,_,stdv,lst = statistics()

	for data in filter(n,maxcnt,stdv,lst, threshold):
		print_post(','.join(data), repo)

	return n

def reference_fragment_index(path):
	lst = []
	for line in open(path):
		id, data = line.strip().split('\t')
		lst += [id]
	return lst

with open(p.repo,'w') as repo:
	post_init(int(p.sample_size), repo)
	report( float(p.organize_threshold), repo )
