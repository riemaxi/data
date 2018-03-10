#!/usr/bin/env  python3

import sys

pos = max(1,int(sys.argv[1])-1)

for line in sys.stdin:
	line = line.strip().split('\t')

	print ( '\t'.join(line[:pos]) )
