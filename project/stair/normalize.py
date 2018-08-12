import sys
import textwrap
from parameter import *

def pack(dna,  zero):
	dna = ''.join(['0' if b in zero else '1'for b in dna])
	return ''.join([ '{:x}'.format(int(b,2)) for b in textwrap.wrap(dna,4)]).upper()

next(sys.stdin).strip()
for line in sys.stdin:
	line = line.strip()
	print(pack(line, p.zero), end = '')
		