def createmask(lst):
	a = [s.strip().split('-') for s in lst]

	a = [{int(s[0])} if len(s)<2 else set(range(int(s[0]), int(s[1]) + 1)) for s in a]

	mask = set()
	for s in a:
		mask = mask | s 

	return sorted(list(mask))

def startprojector(p):
	global mask
	mask = createmask(p.pcriteria.split(','))

def project(row):
	return [row[i] for i in mask]
