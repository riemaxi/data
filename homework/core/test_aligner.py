#!/usr/bin/env python3

import cleanneedle as cn

def align(a,b):
	al = cn.Aligner()
	cn.Tool.printmatrix(al.setmatrix(a,b))
	print()

	for gapsa, gapsb in al.align(a,b):
		da, db = cn.Tool.deployalignment(a,gapsa,b,gapsb)

		print(cn.Tool.alignment2string(da),cn.Tool.alignment2string(db), sep='\n')
		print( al.totalscore(da,db,gapsymbol='_____') )

		print()

align(
	[45,56,34,55,54,45,44,43,32,23,45,67,78],
	[54,45,44,43,32,23,45,67,78]
)

'''
align(
	[45,56,34,55,54,45,44,43,32,23,45,67,78],
	[45,56,34,55,54,         32,23,45,67,78]
)
'''
