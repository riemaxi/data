#!/usr/bin/env python3
import sys

BASE = 'ACGT'

def vector(s):
	v = {'A':0, 'C': 0, 'G': 0, 'T' : 0}
	for b in s:
		v[b] = v.get(b,0) + 1

	return list(v.values())

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv

def read_arg(i, dv):
	try:
		return sys.argv[i]
	except:
		return dv

l = read_int_arg(1,1000)
dest = read_arg(2,'stairified.tsv')

with open(dest, 'w') as f:
	try:
		last = next( sys.stdin ).strip('\n').upper()
		v = vector( last )
		print(0, *v, sep = '\t' )
		f.write( '\t'.join( [str(n) for n in v] ) + '\n' )

		k = 1
		for line in sys.stdin:
			seq = line.strip('\n').upper()

			v = [v[i] - (BASE[i] == last[0]) + (BASE[i] == seq[-1]) for i in range(len(BASE))]
			b = [BASE[i] for i in range(len(BASE)) if BASE[i] == last[0]] + [BASE[i] for i in range(len(BASE)) if BASE[i] == seq[-1]]

			print(k, *b, sep = '\t' )
			f.write( ''.join(b) + '\n' )

			last = seq
			k += 1
	except:
		pass
