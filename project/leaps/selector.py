import sys

def createmask(lst):
	lst = [s.strip().split(':') for s in lst]
	lst = [(int(a),b.split('-')) for a,b in lst]
	mask = {}
	for a,b in lst:
		mask[a] = (int(b[0]),int(b[0])+1) if len(b)==1 else (int(b[0]),int(b[1])+1)

	return mask

def match(row):
	global mask
	for i,c in mask:
		if not int(row[i]) in range(c[0],c[1]):
			return False
	return True

def startselector(p):
	global mask
	mask = createmask(p.scriteria.split(' ')).items()

