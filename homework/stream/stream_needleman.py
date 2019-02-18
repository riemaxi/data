#!/usr/bin/env python3

import http.client
import json
import sys
import random

import binning as b
import stairify as s
import cleanneedle as cn
from parameter import p

def post(data, streamer, event = '/message'):
	try:
		con = http.client.HTTPConnection(streamer)

		headers = {"Content-type": "application/json"}
		con.request('POST', event, json.dumps({"item": data}), headers = headers)

		return True
	except:
		return False


def mutation(a, start, delsize):
	return ''.join(a[:start] + a[start + delsize:])


def generate(size = 10000):
	return ''.join(['ACGT'[random.randint(0,3)] for _ in range(size)])


start = int(sys.argv[1])
delsize = int(sys.argv[2])
size = int(sys.argv[3])

wsize = int(p.window_size)
zero = p.zero
derivative = 1

seqa = generate(size)
seqb = mutation(seqa, start,delsize)

seqa = s.transform(len(seqa), wsize, b.transform(seqa, zero),100,derivative)
seqb = s.transform(len(seqb), wsize, b.transform(seqb, zero),100,derivative)

gapa, gapb = cn.Aligner().align(seqa, seqb)

print(cn.deploy(seqa, gapa), cn.deploy(seqb, gapb), sep='\n')
