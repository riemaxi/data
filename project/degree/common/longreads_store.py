#!/usr/bin/env python3

import sys
from parameter import *

with open(p.longreads_import_dest,'w') as file:
	count = 1
	for line in sys.stdin:
		id, size, data = line.strip().split('\t')

		print(count, id, size, sep= '\t')
		file.write(line)

		count += 1

