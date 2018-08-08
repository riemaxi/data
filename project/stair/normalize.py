import sys
import textwrap

def pack(dna):
	dna = ''.join(['0' if b in ['A','G'] else '1'for b in dna])
	return ''.join([ '{:x}'.format(int(b,2)) for b in textwrap.wrap(dna,4)]).upper()

next(sys.stdin).strip()
for line in sys.stdin:
	line = line.strip()
	print(pack(line), end = '')
		