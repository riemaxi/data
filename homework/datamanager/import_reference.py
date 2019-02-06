#!/usr/bin/env python3

import sys
import binning as b
import stairify as s
from parameter import p

def compress(data, wsize, zero):
	seqsize = len(data)
	data = b.transform(data, zero)
	data = s.transform(seqsize, wsize, data)

	return ' '.join(['{:0.2f}'.format(f) for f in data])

def next_sequence():
	data = []
	for line in sys.stdin:
		line = line.strip()
		if line.startswith('>'):
			return line.split(' ')[0][1:], ''.join(data)

		data += [line]
	return  None, ''.join(data)

wsize = int(p.window_size)
zero = p.zero

id = next(sys.stdin).split(' ')[0][1:]
path = '{}/{}.stair'.format(p.reference, sys.argv[1])
with open(path,'w',buffering = 1) as file:
	while id:
		nextid, data = next_sequence()

		print('compressing ... ',id, len(data), sep = '\t')
		file.write('{}\t{}\n'.format(id, compress(data, wsize, zero)))

		id = nextid
