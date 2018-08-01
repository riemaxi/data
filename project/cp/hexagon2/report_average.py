import os
import sys
import math
from parameter import p

c = 0
fsum = 0
tsum = 0
runs = int(p.runs)

with open('report.tsv', 'w') as file:
	for line in sys.stdin:
		m,s,f,t  = line.strip().split('\t')
		print('{: <3}\t{: <20}\t{: <8}\t{}'.format((c+1)%10 if (c+1)%runs!=0 else runs, m, f, t))
		c += 1	
		
		fsum += int(f)
		tsum += int(t)
	
		if c%runs == 0:
			print('{: >37}\t{: >11}'.format(int(fsum/runs), int(tsum/runs)))
			file.write('{: <20}\t{: <8}\t{}\n'.format(m, int(fsum/runs), int(tsum/runs)))
			fsum = 0
			tsum = 0
