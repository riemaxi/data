
import daemon

class Surrogate(daemon.Daemon):
	def __init__(self, proc):
		daemon.Daemon.__init__(self, proc.pidfile, proc.root, proc.stdin, proc.stdout, proc.stderr)
		self.proc = proc

	def restart(self):
		self.proc.restart()

	def stop(self):
		self.proc.stop()

	def run(self):
		self.proc.run()
