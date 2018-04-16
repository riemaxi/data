#!/usr/bin/env python3

import sys


code_start = int(sys.argv[1])
column = int(sys.argv[2])
sep = sys.argv[3]

code_map = {}

for line in sys.stdin:
	record = line.strip().split(sep)
	key = record[column]

	if code_map.get(key, None) == None:
		code_map[key] = str(code_start)
		code_start += 1

	record[column] = code_map[key]
	print( sep.join(record) )
