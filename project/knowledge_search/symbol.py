#!/usr/bin/env python3

import sys


code_start = int(sys.argv[1])
column = int(sys.argv[2])
sep = sys.argv[3]
symbol = sys.argv[4]

code_map = {}

for line in sys.stdin:
	record = line.strip().split(sep)
	key = record[column]

	if code_map.get(key, None) == None:
		code_map[key] = str(code_start)
		code_start += 1

	record[column] = code_map[key]
	print( sep.join(record) )

with open(symbol, 'w') as f:
	f.write('\n'.join(['{}\t{}\t{}'.format(column,key,value) for key,value in code_map.items()]) + '\n')
