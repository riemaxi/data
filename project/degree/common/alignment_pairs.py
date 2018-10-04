import itertools as it

def pairs(patha, pathb):
	for a,b in it.product(open(patha), open(pathb)):
		yield a,b
