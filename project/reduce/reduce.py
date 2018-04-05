#!/usr/bin/env python3
import sys

def Counter(s):
	count = {'A':0, 'C': 0, 'G': 0, 'T' : 0}
	for b in s:
		count[b] = count.get(b,0) + 1

	return count.items()

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv

l = read_int_arg(1,1000)
max_section = read_int_arg(2,9)

i = 1
for line in sys.stdin:
	seq = line.strip().upper()
	count = Counter( seq )
	print(i, '\t'.join([str(int( max_section * c/l )) for a,c in count]), sep = '\t' )

	i += 1
