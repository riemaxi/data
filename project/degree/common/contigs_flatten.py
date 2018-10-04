#!/usr/bin/env python3

import sys

print( next(sys.stdin).strip(), end='\t' )
for line in sys.stdin:
	if line.startswith('>'):
		print()
		print(line.strip(), end='\t')
	else:
		print(line.strip(), end='')

