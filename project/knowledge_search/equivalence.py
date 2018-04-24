#!/usr/bin/env python3

import sys

def print_class(key, lst):
	print(key, lst[0], ','.join([str(n) for n in lst]), sep = '\t')


lastkey, id, member = next(sys.stdin).strip().split('\t')
eclass = {lastkey: {int(id), int(member)}}

for line in sys.stdin:
	key, id, member =  line.strip().split('\t')

	if key != lastkey:
		print_class( lastkey, sorted(list(eclass[lastkey])) )

		eclass = {key: {int(id), int(member)}}
		lastkey = key
	else:
		eclass[key] = eclass[key] | {int(id),int(member)}

print_class( lastkey, sorted(list(eclass[lastkey])) )
