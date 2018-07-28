import sys
import math

r = {}
for line in sys.stdin:
	line = line.strip().split(":",2)
	if len(line) and line[0].strip() in ('size','runtime','failures','model'):
		r[line[0].strip()] = line[1].strip()
		
		if len(r) == 4:
			time = float(r['runtime'].split(' ',1)[1][1:-4])
			ms,s = math.modf(time/1000)
			
			print('{: <10}\t{: <6}\t{: <10}\t{}'.format( r['model'], r['size'], r['failures'], '{:.1f}'.format(int(s), int(ms*1000)) ) )
			r = {}
		