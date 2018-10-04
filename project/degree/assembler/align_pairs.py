#!/usr/bin/env python3

import os
import sys
import itertools as it
import time
import threading
import queue

import alignment as al
from parameter import *


class AlignProcess(threading.Thread):
	def __init__(self,ida,idb, sizea,sizeb, seqa, seqb, tolerance, printer):
		threading.Thread.__init__(self)

		self.sizea,self.sizeb = sizea,sizeb
		self.ida, self.idb = ida,idb
		self.seqa, self.seqb = seqa, seqb

		self.tolerance = tolerance

		self.printer = printer

		self.start()

	def run(self):
		ida,idb = self.ida, self.idb

		sizea,sizeb = self.sizea, self.sizeb

		try:
			start = time.time()
			number, gaps1, gaps2,j,i = al.Realwater(0,0,len(self.seqa),len(self.seqb),self.tolerance).align(self.seqa, self.seqb)
			elapsed = time.time() - start

			self.printer.qprint([ elapsed,[number[0],number[1]], [ida,sizea,j, str(gaps1)[1:-1]], [idb, sizeb,i, str(gaps2)[1:-1]] ])
		except Exception as e:
			self.printer.qprint([0,[0,0],[ida,sizea,0,e],[idb,sizeb,0,e]])


class PrinterQueue(threading.Thread):
	def __init__(self, dest):
		threading.Thread.__init__(self)
		self.queue = queue.Queue()
		self.dest = dest

		self.start()

	def qprint(self, data):
		self.queue.put(data)

	def run(self):
		with open(self.dest,'w',buffering=1) as dest:
			while True:
				while not self.queue.empty():
					data = self.queue.get()
					elapsed = data[0]

					identity, score = data[1][0], data[1][1]

					ida, idb = data[2][0], data[3][0]
					sizea, sizeb = data[2][1], data[3][1]

					j,i = data[2][2], data[3][2]
					gapsa,gapsb = data[2][3], data[3][3]

					line = '{:0.2f}\n{:0.2f}\t{:0.2f}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n'.format(elapsed,identity, score,ida,idb,sizea,sizeb,j,gapsa,i,gapsb)

					dest.write(line)
					print('{}\t{}\t{:0.2f}\t{:0.2f}'.format(ida,idb, identity,score), flush=True)

			time.sleep(2)



RECORD_SIZE = 2

def nextrecord(input, rs):
	return [x.strip() for x in it.islice(input,rs)]



os.system('mkdir -p {}'.format(p.report_folder))
printer = PrinterQueue(p.report_dest.format(p.report_folder))

r = nextrecord(sys.stdin, RECORD_SIZE)
while r:
	ida, sizea, dataa = r[0].split('\t',2)
	idb, sizeb, datab = r[1].split('\t',2)

	try:
		a = [float(f) for f in dataa.split()]
		b = [float(f) for f in datab.split()]

		AlignProcess(ida,idb,int(sizea), int(sizeb), a,b, float(p.tolerance), printer)

		r = nextrecord(sys.stdin, RECORD_SIZE)
	except:
		r = None





