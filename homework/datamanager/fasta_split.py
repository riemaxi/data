#!/usr/bin/env python3

import sys

def writefile(outpath, prefix, id, data):
	open('{}/{}_{}.flast'.format(outpath, prefix, id),'w').write(''.join(data))


inpath = sys.argv[1]
outpath = sys.argv[2]
prefix = sys.argv[3]

with open(inpath) as infile:
	next(infile)
	id = 0
	data = []
	for line in infile:
		line = line.strip()
		if line.startswith('>'):
			writefile(outpath, prefix,id, data)

			id += 1
			data = []
		else:
			data += [line]


writefile(outpath, prefix,id, data)
