#!/usr/bin/env python3

import dataset as ds
from parameter import p
import sys

reference = p.reference

path = '{}/{}.stair'.format(reference, sys.argv[1])
with open(sys.argv[2],'w') as file:
	for r in ds.records(input = open(path)):
		id, data = r[0].split('\t')
		data = data[1:-1].replace("'",'')
		print(id)

		file.write('{}\t{}\n'.format(id, data))
