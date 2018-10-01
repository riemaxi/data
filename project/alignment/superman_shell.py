#!/usr/bin/env python3

import superman as al

sm = al.Littleman()

aseq = [1,2,3,4,5,6,7,8,20,34]
bseq = [3,4,5,6,7,8,9,0,10,20,34]

for a,b in sm.alignment(aseq,bseq):
	print(*a, sep='\t')
	print(*b, sep='\t')
	print()
