import os
import sys
import math

r = {}
for line in sys.stdin:
	line = line.strip().split(":",1)

	if len(line) and line[0].strip() in ('runtime','failures','model','solutions', 'first'):
		r[line[0].strip()] = line[1].strip()
		
		if len(r) == 5:
			time = float(r['runtime'].split(' ',1)[1][1:-4])
			ms,s = math.modf(time/1000)
			
			print('{: <10}\t{: <6}\t{: <10}\t{: <8}\t{}'.format( r['model'], r['solutions'], r['failures'], int(ms*1000), r['first']) )
			sys.stdout.flush()			
			r = {}
			