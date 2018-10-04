import queue
import threading
import time

class Reporter(threading.Thread):
	def __init__(self, dest):
		threading.Thread.__init__(self)
		self.queue = queue.Queue()
		self.dest = dest

		self.start()

	def report(self, data):
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
					a,b = data[2][3], data[3][3]

					line = '{:0.2f}\n{:0.2f}\t{:0.2f}\n{}\t{}\n{}\t{}\n{}\t{}\n{}\t{}\n'.format(elapsed,identity, score,ida,idb,sizea,sizeb,j,a,i,b)

					print(ida,idb,sep='\t', flush=True)

					dest.write(line)

				time.sleep(2)
