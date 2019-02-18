#!/usr/bin/env python3

import http.client
import urllib
import json
from parameter import p


def post(data, streamer, event = '/message'):
	try:
		con = http.client.HTTPConnection(streamer)

		headers = {"Content-type": "application/json"}
		con.request('POST', event, json.dumps({"item": data}), headers = headers)

		return True
	except:
		return False

def post_init(sample_size):
	data = {'rfidx' : reference_fragment_index(p.hot_reference), 'sample_size' : sample_size }
	post(data, p.organize_streamer, '/init')

def getInitialisation(data):
	sample_size, reference = data.split('\t')
	return {
		'sample_size' : int(sample_size),
		'rfidx' : reference.split(',')
	}


def getRecord(data):
	rid,qid,cnt,rstart,rend,qstart,qend,score = data.split(',')
	return rid,int(qid),int(cnt),int(rstart),int(rend),int(qstart),int(qend),float(score)

with open(p.repo) as repo:
	data = getInitialisation(next(repo).strip())
	post(data, p.organize_streamer, '/init')

	for line in repo:
		rid,qid,cnt,rstart,rend,qstart,qend,score = getRecord(line.strip())
		post((rid,qid,cnt,rstart,rend,qstart,qend,score), p.organize_streamer)
