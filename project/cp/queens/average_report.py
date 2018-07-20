
import sys

next(sys.stdin)
next(sys.stdin)

idx = 0
for line in sys.stdin:
	average, time = line.strip().split('\t')[-2:]
	
	if float(time.split(';')[1]) > 0:
		print(idx, *average.split(';'), sep = '\t')
		idx += 1