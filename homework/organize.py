#!/usr/bin/env python3

import http.client, urllib
import time
import os
import math
import json
from parameter import p

def stdv(mean,n, lst, field = 3):
	return math.sqrt( sum([(float(r[field])-mean)**2 for r in lst])/(n-1) )

def statistics(dataset):
	totalcnt = 0
	maxcnt = float('-inf')
	lst = []
	for line in dataset:
		rid, qid,cnt, rstart, rend, qstart,qend, score,_ = line.strip().split('\t')

		totalcnt += int(cnt)
		maxcnt = max(maxcnt, int(cnt))
		lst += [(rid, qid, cnt, rstart, rend, qstart, qend, score)]

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
				yield rid, int(qid), cnt, int(rstart), int(rend), int(qstart), int(qend), score

def post(data, streamer, event = '/message'):
	try:
		con = http.client.HTTPConnection(streamer)

		headers = {"Content-type": "application/json"}
		con.request('POST', event, json.dumps({"item": data}), headers = headers)

		return True
	except Exception as e:
		return False

def report(path, streamer, threshold):
	n,maxcnt,_,stdv,lst = statistics(open(path))
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
	return count == size

open('process.pid','a').write('{}\n'.format(os.getpid()))

bedtime = int(p.organize_bedtime)

ref_frag = reference_fragment_index(p.hot_reference)
post(ref_frag, p.organize_streamer, '/init')

while True:
	try:
		if os.path.isfile(p.lookup_outpath) and lookup_ready(p.lookup_outpath, len(ref_frag) * int(p.sample_size)):
				os.system('cp {} {}'.format(p.lookup_outpath, p.organize_report_path))

				report(p.organize_report_path, p.organize_streamer, float(p.organize_threshold))

				os.system('rm -f {}'.format(p.organize_report_path))

				break

		time.sleep(bedtime)
	except Exception as e:
		print(e)
		break
