#!/usr/bin/env python3

import cleanneedle as cn

def align(a,ga, b, gb):
	print(cn.Tool.deploys(a,ga), cn.Tool.deploys(b,gb), sep='\n')

	al = cn.Aligner()
	cn.Tool.printmatrix(al.setmatrix(a,b))
	print()

	for da,db,s in cn.Tool.topalignments(al.deployments(a,b, False), 0.1, 25):
		print(da, db, sep='\n')
		print(s)

		print()


align(
	[45,56,34,55,54,45,44,43,32,23,45,67,78], {},
	[            54,45,44,43,32,23,45,67,78], {0:4}
)


'''
align(
	[45,56,34,55,54,45,44,43,32,23,45,67,78],
	[45,56,34,55,54,         32,23,45,67,78]
)
'''
