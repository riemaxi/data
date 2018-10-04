#!/usr/bin/env python3

from alignment import *


data1 = '57.1	56.1	52.7	56.3	59.4	57.3	57.5	59.4	59.4	58.9	61.1	60.7	60.0	60.5	63.9	66.8'
data2 = '52.7	56.3	59.4	57.3	59.4	58.9	61.1	60.7	60.0	60.5	63.9	66.8'
#data2 = '57.3	57.5	59.4	59.4	58.9	61.1	60.7	60.0	60.5	63.9	66.8'
#data2 = '57.1	56.1	52.7	56.3	59.4	57.3	57.5	59.4	59.4	58.9	61.1'

seq1 = [float(f) for f in data1.split('\t')]
pos1 = 0
size1 = len(seq1)

seq2 = [float(f) for f in data2.split('\t')]
size2 = len(seq2)
pos2 = 0


for number, gaps1, gaps2 in Realmen(pos1,pos2,size1,size2,0.1).alignment(seq1, seq2):
	print('{:0.2f}\t{:0.2f}'.format(*number))
	print(*Tool.ideploy(seq1, pos1, size1, gaps1), sep='\t')
	print(*Tool.ideploy(seq2, pos2, size2, gaps2), sep='\t')

