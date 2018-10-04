import os

class PipeProcess:
	def __init__(self):
		self.pidfile = 'log/pipeline.pid'
		self.root = './'
		self.stdin =  '/dev/null'
		self.stdout = 'log/pipeline.out'
		self.stderr = 'log/pipeline.err'

	def run(self):
		os.system('./pipeline.sh')
