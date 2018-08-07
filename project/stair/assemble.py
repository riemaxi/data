import sys

def print_contig(idx, path):
	with open(path) as f:
		for i,line in enumerate(f):
			line = line.strip().split('\t')
			if idx == int(line[0]):
				print(line[1], end = '')
			

for line in sys.stdin:
	idx = int(line.strip())
	print_contig(idx, sys.argv[1])
	