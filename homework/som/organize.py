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
				yield int(rid), qid, cnt, int(rstart), int(rend), int(qstart), int(qend), score

def post(data, streamer):
	try:
		con = http.client.HTTPConnection(streamer)

		headers = {"Content-type": "application/json"}
		con.request('POST', '/message', json.dumps({"item": data}), headers = headers)
	except Exception as e:
		print(e)

def report(path, streamer, threshold):
	n,maxcnt,_,stdv,lst = statistics(open(path))
	for rid, qid, cnt, rstart, rend, qstart, qend, score in filter(n,maxcnt,stdv,lst, threshold):
		post([rid,qid,cnt,rstart,rend,qstart,qend,score], streamer)
	return n

open('process.pid','w').write(str(os.getpid()))

bedtime = int(p.bedtime)

while True:
	try:
		os.system('cp {} {}'.format(p.score_path, p.report_path))

		report(p.report_path, p.streamer, float(p.threshold))

		os.system('rm -f {}'.format(p.report_path))
		time.sleep(bedtime)
	except Exception as e:
		print(e)
		break
