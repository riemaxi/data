#!/usr/bin/env python3
import http.client, urllib.parse
import json
import os

import dataset as ds
import binning as b
import stairify as s
from parameter import p

def stairify(data, window_size, zero, base = 100):
	return s.transform(len(data), window_size, b.transform(data, zero))

def stair2str(data, template):
	return ' '.join([template.format(f) for f in data])

def post(id, data, host):
	try:
		con = http.client.HTTPConnection(host)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		data = {'id' : id, 'data' : data.split(' ')}
		con.request('POST', '/data', body = json.dumps(data), headers = headers)
	except:
		pass

open('process.pid','a').write('{}\n'.format(os.getpid()))

hosts = p.hosts.split(',')
window_size = int(p.window_size)
zero = p.zero
template = '{:.PRECISIONf}'.replace('PRECISION',p.precision)

idx = 0
for r in ds.records():
	id, data = r[0].split('\t')

	post(id, stair2str(stairify(data, window_size, zero), template), hosts[idx])

	idx = (idx + 1) % len(hosts)
