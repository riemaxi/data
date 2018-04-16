#!/usr/bin/env python3

import sys

sep = ','

jump = 1
for a in sys.stdin:
	a = a.strip().split(sep)
	
	with open(sys.argv[1]) as file:
		for _ in range(jump):
			next(file)

		for b in file:
			b = b.strip().split(sep)

			print(sep.join(a),sep.join(b), sep = '\t')

	jump += 1


