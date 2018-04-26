#!/usr/bin/env python3

import sys

def print_record(record):
	for c,v in record.items():
		print('{}'.format(v), end = '\t')
	print()

def print_header(record):
	for c in record.items():
		print('{}'.format(c), end = '\t')
	print()



sep = ' '

last, p, pv,type, t, data = (next(sys.stdin).strip().split(sep))
record = {'a': last, 'b': type, 'c': t, 'd': data, p: pv}

for line in sys.stdin:
	id, p, pv,type, t, data = line.strip().split(sep)
	record[p] = pv

	if id != last:
		print_record(record)
		record = {'a': id,'b': type, 'c': t, 'd': data, p: pv}

		last = id

print_record(record)

