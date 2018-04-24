#!/usr/bin/env python3

import sys

for line in sys.stdin:
	spair =  line.strip().split('\t')
	a,b = [set([int(n) for n in s.split(',')]) for s in spair]

	if a <= b:
		print(*sorted(list(a)), sep=',')
	else:
		if b < a:
			print(*sorted(list(b)), sep=',')
		else:
			print(*sorted(list(a | b)), sep = ',')

