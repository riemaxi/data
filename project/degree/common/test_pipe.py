#!/usr/bin/env python3

from alignment import *
import stairify as stairs

id, seqsize, data = next(open('data/binning_reference.AT.dat')).strip().split('\t')
ref = stairs.transform(id,int(seqsize),100,data)
pos = 0
size = len(ref)


for line in open('data/binning_contig.AT.dat'):
	id1, seqsize1, data = line.strip().split('\t')
	seq1 = stairs.transform(id,int(seqsize),100,data)
	pos1 = 0
	size1 = len(seq1)

	number, gaps, gaps1 = Realman(pos,pos1,size,size1,2.0).align(ref, seq1)

	print(number, size, size1)
