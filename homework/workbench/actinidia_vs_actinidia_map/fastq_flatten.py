#!/usr/bin/env python3

import sys
import dataset as ds

inpath = sys.argv[1]
outpath = sys.argv[2]
name = sys.argv[3]

id = 0
with open('{}/{}.flast'.format(outpath, name),'w') as file:
	for r in ds.records(input= open(inpath), rs=4):
		file.write('{}\t{}\n'.format(id, r[1]))
		print(id, r[1][:100], len(r[1]))

		id += 1
