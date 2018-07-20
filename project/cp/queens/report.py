
import sys
import os
import math

def aggregate(line):
	v = [(float(a), int(b), int(s)) for a,b,s in [s.split(';') for s in line]]
	
	ra = sum([a for a,b,c in v])/len(v)
	fa = int(sum([b for a,b,c in v])/len(v))
	sa = sum([c for a,b,c in v])/len(v)
	
	ms,s = math.modf(ra/1000)
	
	return '\t'.join(['{: <20}'.format(s) for s in line]), '{};{}'.format(ra,fa,sa), '{}:{};{:.1f}'.format(int(s), int(ms*1000), sa)
	
	
def mode(path, runs):
	if os.path.exists(path):
		return 'a', ''
	else:
		return 'w', '{}\t{: <4}\t{: <10}\t{: <20}\t{: <10}\n'.format('#', 'size', '\t'.join(['{: <20}'.format(i+1) for i in range(runs)]) , 'average','average(s:ms)')
	
def size(start, step, i):
	return start + step*i

start = int(sys.argv[1])
step = int(sys.argv[2])
startsize = int(sys.argv[3])
runs = int(sys.argv[4])
path = sys.argv[5]

i = start
m, header = mode(path, runs)
with open(path, m) as file:
	file.write(header);
	for line in sys.stdin:
		line = line.strip().split('\t')
		
		v,a,rt_sol =  aggregate(line)

		file.write('{}\t{: <4}\t{: <10}\t{: <20}\t{: <10}\n'.format(i, startsize + step*i, v, a,rt_sol))

		r,f = a.split(';')
		print('{}\t{: <4}\t{: <10}\t{: <10}'.format(i, startsize + step*i, r, f ))
		
		i += 1

		
