#!/usr/bin/env python3

import http.client, urllib
import time
import os
import sys
import math
import json
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
		lst += [(rid, int(qid), int(cnt), int(rstart), int(rend), int(qstart), int(qend), float(score))]

	n = len(lst)
	if n>1:
		return n, maxcnt, totalcnt/n, stdv(totalcnt/n, n, lst), lst
	else:
		return 0, 0,0,0, []


def level(cnt,maxcnt, stdvc):
	return stdvc/(abs(maxcnt - cnt) + stdvc)
	#return 1/(0.5 * stdvc * abs(maxcnt - cnt) + 1)


def filter(n, maxcnt, stdv, lst, threshold = 0.3):
	for rid, qid, cnt, rstart, rend, qstart, qend, score in lst:
		if cnt>0:
			score = (score/cnt) * level(cnt, maxcnt, stdv)
			if score >= threshold:
				yield rid, qid, cnt, rstart, rend, qstart, qend, score

def post(data, streamer, event = '/message'):
	try:
		con = http.client.HTTPConnection(streamer)

		headers = {"Content-type": "application/json"}
		con.request('POST', event, json.dumps({"item": data}), headers = headers)

		print(*data, sep='\t', flush = True)

		return True
	except Exception as e:
		return False

def post_init(size):
	data = {'rfidx' : reference_fragment_index(p.hot_reference), 'size'  : size }
	post(data, p.organize_streamer, '/init')

def report(streamer, threshold):
	n,maxcnt,_,stdv,lst = statistics()

	post_init(n)


	for rid, qid, cnt, rstart, rend, qstart, qend, score in filter(n,maxcnt,stdv,lst, threshold):
		post((rid,qid,cnt,rstart,rend,qstart,qend,score), streamer)
	return n

def reference_fragment_index(path):
	lst = []
	for line in open(path):
		id, data = line.strip().split('\t')
		lst += [id]
	return lst

def lookup_ready(path, size):
	count = 0
	for _ in open(path):
		count += 1
	open('log/counter.txt','w').write(str(count) + ' , ' + str(size))
	return count >= size

report( p.organize_streamer, float(p.organize_threshold))
