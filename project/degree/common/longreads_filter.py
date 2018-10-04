#!/usr/bin/python3 -u

import sys
import itertools as it
from parameter import *

RECORD_SIZE = 4

def nextrecord():
	return [x.strip() for x in it.islice(sys.stdin,RECORD_SIZE)]

def quality(line):
	return int(sum([ord(a)-33 for a in line])/len(line))

qmin = int(p.longreads_import_quality)

record = nextrecord()

while record:
	q = quality(record[3])
	if q>=qmin:
		print(record[0].split()[0], len(record[1]), record[1], sep = '\t')

	record = nextrecord()
