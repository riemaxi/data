import os
import sys
import math

r = {}
for line in sys.stdin:
	line = line.strip().split(":",1)

	if len(line) and line[0].strip() in ('runtime','failures','size','solutions', 'run'):
		r[line[0].strip()] = line[1].strip()
		
		if len(r) == 5:
			time = float(r['runtime'].split(' ',1)[1][1:-4])
			
			print('{: >4}\t{: <4}\t{: <10}\t{: <10}\t{}'.format(r['run'], r['size'],r['failures'],r['solutions'], time))
			sys.stdout.flush()			
			r = {}
			