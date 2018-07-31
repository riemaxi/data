import os
import sys
import math

r = {}
with open('report.tsv', 'w') as file:
	for line in sys.stdin:
		line = line.strip().split(":",1)
		if len(line) and line[0].strip() in ('runtime','failures','model','solutions'):
			r[line[0].strip()] = line[1].strip()
			
			if len(r) == 4:
				time = float(r['runtime'].split(' ',1)[1][1:-4])
				ms,s = math.modf(time/1000)
				
				print('{: <10}\t{: <6}\t{: <10}\t{}'.format( r['model'], r['solutions'], r['failures'], '{:.1f}'.format(int(s), int(ms*1000)) ) )
				file.write('{: <10}\t{: <6}\t{: <10}\t{}\n'.format( r['model'], r['solutions'], r['failures'], '{:.1f}'.format(int(s), int(ms*1000)) )  )
				file.flush()
				os.fsync(file)
				r = {}
			