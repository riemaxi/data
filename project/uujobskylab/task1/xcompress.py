#!/usr/bin/env python3

import gzip
import sys

dest = sys.argv[1]

with gzip.open(dest,'wb') as f:
	for line in sys.stdin:
		print(line.strip())
		f.write(bytearray(line,'utf8'))
