#!/usr/bin/env python3

import http.server
import socketserver
import json
import sys
import os
import time

import clearwater as cw
from parameter import p

class Tool:
	def reference_fragments():
		for line in open(p.hot_reference):
			id,f = line.strip().split('\t')
			yield id, Tool.tofloat(f.split(' '))

	def tofloat( data):
		return [float(f) for f in data]


class Handler(http.server.BaseHTTPRequestHandler):


	def lookup_and_report(self, qid, qdata):
		global outpath
		global reference_fragments

		for rid, rdata in Tool.reference_fragments():
			try:
				starttime = time.time()
				(scr,(rstart,rend),(qstart,qend), cnt),_ = cw.Warmmapper().map(rdata, qdata)
				elapsed = time.time() - starttime

				screport = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(rid, qid, cnt, rstart, rend, qstart, qend, '{:0.2f}\t{:0.5f}'.format(scr, elapsed))

				open('{}/score.out'.format(outpath),'a').write(screport)
			except Exception as e:
				open('log/error.log','a').write('{}\n'.format(e))


	def do_POST(self):

		length = int(self.headers.get('Content-Length'))
		body = self.rfile.read(length).decode('utf-8')
		body = json.JSONDecoder().decode(body)

		self.lookup_and_report(body['id'],Tool.tofloat(body['data']))



open('process.pid','a').write('{}\n'.format(os.getpid()))

port = int(p.port)
outpath = p.outpath

with socketserver.TCPServer(("", port), Handler) as httpd:
    httpd.serve_forever()
