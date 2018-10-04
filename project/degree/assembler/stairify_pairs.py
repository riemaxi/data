#!/usr/bin/env python3

import sys
import itertools as it
import stairify as stairs
from parameter import *

RECORD_SIZE = 2

def nextrecord(input, rs):
	return [x.strip() for x in it.islice(input,rs)]

window = int(p.window)

r = nextrecord(sys.stdin, RECORD_SIZE)
while r:
	ida, sizea, dataa = r[0].split()
	idb, sizeb, datab = r[1].split()

	try:
		print(ida, sizea, *stairs.transform(ida, int(sizea),window , dataa), sep='\t')
		print(idb, sizeb, *stairs.transform(idb, int(sizeb),window, datab), sep='\t')

		r = nextrecord(sys.stdin, RECORD_SIZE)
	except:
		r = None





