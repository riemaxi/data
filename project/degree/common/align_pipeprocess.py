#!/usr/bin/env python3

import alignment_process as prc
import alignment_pairs  as ap
import alignment_reporter as ar
from parameter import *
import os

class PipeProcess:
	def __init__(self):
		self.pidfile = 'log/align_pipeprocess.pid'
		self.root = './'
		self.stdin =  '/dev/null'
		self.stdout = 'log/align_pipeprocess.out'
		self.stderr = 'log/align_pipeprocess.err'

	def run(self):
		os.system('mkdir -p {}'.format(p.report_folder))
		reporter = ar.Reporter(p.report_dest.format(p.report_folder))
		for a,b in ap.pairs(p.contigs_binning_dest.format(p.zero), p.longreads_binning_dest.format(p.zero)):
			prc.AlignProcess(a,b, reporter)
