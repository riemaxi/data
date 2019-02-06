#!/usr/bin/env python3

import http.server
import socketserver
import json
import sys
import os
import time

import clearwater as cw
from parameter import p


class Handler(http.server.BaseHTTPRequestHandler):

	def tofloat(self, data):
		return [float(f) for f in data]

	def load_fragments(self):
		for line in open(self.reference):
			id,i,f = line.strip().split('\t')
			lst += [id,i, self.tofloat(f)]

		return lst

	def lookup_and_report(self, qid, qdata):
		global outpath
		global port

		for rid,i,rdata in self.fragments:
			starttime = time.time()
			(scr,(rstart,rend),(qstart,qend), cnt),_ = cw.Warmmapper().map(rdata, qdata)
			elapsed = time.time() - starttime

			screport = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('{}\t{}'.format(rid,i), qid, cnt, rstart, rend, qstart, qend, '{:0.2f}\t{:0.5f}'.format(scr, elapsed))

			open('{}/score_{}.out'.format(outpath, port),'a').write(screport)


	def do_POST(self):

		length = int(self.headers.get('Content-Length'))
		body = self.rfile.read(length).decode('utf-8')
		body = json.JSONDecoder().decode(body)

		if body.get('init'):
			self.reference = body['reference']
			self.load_fragments()
		else:
			self.lookup_and_report(self.tofloat(body['data']))

open('process.pid','a').write('{}\n'.format(os.getpid()))

port = int(sys.argv[1])
outpath = p.outpath


with socketserver.TCPServer(("", port), Handler) as httpd:
    httpd.serve_forever()


