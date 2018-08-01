import os
import sys
import math
from parameter import p

c = 0
fsum = 0
tsum = 0
ssum = 0
runs = int(p.runs)

with open('report.tsv', 'w') as file:
	for line in sys.stdin:
		m,s,f,t  = line.strip().split('\t')
		print('{: <3}\t{}\t{: <20}\t{: <8}\t{}'.format((c+1)%10 if (c+1)%runs!=0 else runs, s, m, f, t))
		c += 1	
		
		fsum += int(f)
		tsum += int(t)
		ssum += int(s)
	
		if c%runs == 0:
			print('{: >9}\t{: >28}\t{: >10}'.format(int(ssum/runs),int(fsum/runs), int(tsum/runs)))
			file.write('{: <20}\t{: <8}\t{: <8}\t{}\n'.format(m, int(ssum/runs), int(fsum/runs), int(tsum/runs)))
			fsum, tsum,	ssum = [0,0,0]
