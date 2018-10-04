#!/usr/bin/env python3

import binning
from parameter import *

class Sink:
	def __init__(self, repo):
		self.repo = repo

	def tail(self,data):
		self.repo.write(data)

	def head(self,id, size):
		print('{}\t{}\t'.format(id, size))
		self.repo.write('{}\t{}\t'.format(id, size))

	def end(self):
		self.repo.write('\n')


for zero in p.zero.split(','):
	repo = open(p.longreads_binning_dest.format(zero),'w')
	sink = Sink(repo)
	for line in open(p.longreads_import_dest):
		id, seqsize, data = line.strip().split('\t')
		binning.binn(id,seqsize, data, zero, sink)
	repo.close()
