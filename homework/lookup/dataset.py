# This software has been writen by Samuel Ferrer
# ferraxi@gmail.com
# copyright © 2018

# The functions on this file encapsulate the itertools API

import sys
import itertools as it

OK = lambda r : True
END = lambda r : False

RECORD_SIZE = 1

def records(input = sys.stdin, rs = RECORD_SIZE, ok = OK, end = END):

	def nextrecord(input, rs):
		try:
			return [x.strip() for x in it.islice(input,rs)]
		except:
			return None

	r = nextrecord(input, rs)
	while r:
		if ok(r):
			yield r

		r = None if end(r) else nextrecord(input, rs)

def pairs(inputa = sys.stdin,inputb=sys.stdin, rs=1):
	for a,b in  it.product(records(inputa,rs), records(inputb,rs)):
		yield a,b

def join(inputa = sys.stdin,inputb=sys.stdin, rs=1):
	def nextpair(aiter, biter):
		a,b = next(aiter), next(biter)
		return a,b if a and b else None

	aiter = records(inputa,rs)
	biter = records(inputb,rs)

	pair = nextpair(aiter, biter)
	while pair:
		yield pair
		pair = nextpair(aiter, biter)

