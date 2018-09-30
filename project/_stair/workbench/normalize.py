import sys
import textwrap

def pack(dna):
	dna = ''.join(['0' if b in ['A','G'] else '1'for b in dna])
	return ''.join([ '{:x}'.format(int(b,2)) for b in textwrap.wrap(dna,4)]).upper()

def index(line):
	try:
		return line.split()[0].split('_')[2] + '\t'
	except:
		return ''
	
	
line = next(sys.stdin).strip()
print(index(line), end = '')

for line in sys.stdin:
	line = line.strip()
	if line.startswith('>'):
		print('\n{}'.format(index(line)), end = '')
	else:
		print(pack(line), end = '')
		