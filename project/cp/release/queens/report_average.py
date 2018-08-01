import sys
import math
import os
from parameter import p

fsum, ssum, tsum = [0,0,0]
runs = int(p.runs)
with open('report.tsv','w') as file:
	for line in sys.stdin:
		r, s, f, sol, t = line.strip().split('\t')
		print('{: <4}\t{: <20}\t{: <20}\t{}'.format(r, f, s, t))
		
		fsum, tsum , ssum = [fsum + int(f), tsum + float(t), ssum + int(s)]
		
		if int(r) == runs:
			ms,sc = math.modf(tsum/(runs*1000))

			print('{: >4}\t{: <20}\t{: <20}'.format(s,int(fsum/runs),'{:.1f}'.format(int(sc), int(ms*1000))))
			file.write('{: >4}\t{: <20}\t{: <20}\n'.format(s,int(fsum/runs),'{:.1f}'.format(int(sc), int(ms*1000))))
			file.flush()
			os.fsync(file)
			
			fsum, ssum, tsum = [0,0,0]