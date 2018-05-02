#!/usr/bin/env python3

import sys
from projector import startprojector, project
from parameter import p

sep = '\t'

startprojector(p)
for line in sys.stdin:
	row = line.strip().split(sep)

	print( '\t'.join( project(row) ) )
