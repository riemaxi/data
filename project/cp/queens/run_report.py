import sys

def report(line, m, items, runs):
	r = line.split(':',1)
	m[r[0]] = r[1].strip()

	if len(m) == 3:
		item = '{};{};{}'.format(m['runtime'].split(' ',1)[1][1:-4], m['failures'], m['solutions'])
		items.append(item)
		m = {}
		
	if len(items) == runs:
		print('\t'.join(items))
		items.clear()
		
	
	return m


runs = int(sys.argv[1])
m = {}
items = []
for line in sys.stdin:
		line = line.strip()
		if line.startswith('runtime:') or line.startswith('failures:') or line.startswith('solutions:'):
			m = report(line, m, items, runs)
