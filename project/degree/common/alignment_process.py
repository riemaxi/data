import stairify as stairs
import threading
import alignment as al
import time

class AlignProcess(threading.Thread):
	def __init__(self, seqa, seqb, reporter):
		threading.Thread.__init__(self)

		self.seqa = seqa
		self.seqb = seqb
		self.reporter = reporter

		self.window = 100
		self.minsize = 1000
		self.tolerance = 2.0

		self.start()

	def run(self):
		ida, sizea, dataa = self.seqa.split()
		idb, sizeb, datab = self.seqb.split()

		sizea,sizeb = int(sizea), int(sizeb)

		if sizea >= self.minsize and sizeb >= self.minsize:
			a = stairs.transform(ida, sizea, self.window, dataa)
			b = stairs.transform(idb, sizeb, self.window, datab)

			try:
				start = time.time()
				number, gaps1, gaps2,j,i = al.Realwater(0,0,len(a),len(b),self.tolerance).align(a, b)
				elapsed = time.time() - start

				self.reporter.report([ elapsed,[number[0],number[1]], [ida,sizea,j, str(gaps1)[1:-1]], [idb, sizeb,i, str(gaps2)[1:-1]] ])
			except Exception as e:
				self.reporter.report([0,[0,0],[ida,sizea,0,e],[idb,sizeb,0,e]])
