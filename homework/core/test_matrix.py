#!/usr/bin/env python3

import cleanneedle as cn

def test(a,ga,b,gb):

	al = cn.Aligner( cn.Setting(match_factor = 20) )

	print(*cn.Tool.deploy(a, ga, symbol='--'))
	print(*cn.Tool.deploy(b, gb, symbol='--'))


	cn.Tool.printmatrix(al.setmatrix(a,b))


test(
	[45,56,34,55,54,45,44,43,32,23,45,67,78],{},
	[            54,45,44,43,32,23,45,67,78],{0:4}
)

'''
test(
	[45,56,34,55,54,45,44,43,32,23,45,67,78],{},
	[45,56,34,55,54,         32,23,45,67,78],{5:3}

)
'''
