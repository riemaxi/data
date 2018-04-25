from collections import namedtuple
import sys

def readarg(i, dv = ''):
	try:
		return sys.argv[i]
	except:
		return dv

def load():
	path = readarg(1,'parameter.data')
	sep = readarg(2, '=')
	comment = readarg(3,'#')

	setting = {}
	with open(path) as f:
		for pair in f.read().split('\n'):
			pair = pair.strip()
			if pair and not pair.startswith(comment):
				field, value = pair.split(sep)
				setting[field.strip()] = value.strip()

	return ','.join(setting.keys()), setting


fields, setting = load()

DefaultParameter = namedtuple('DefaultParameter',fields)

class Parameter(DefaultParameter):
	def __new__(self, setting):
		return super(Parameter, self).__new__(self, **setting)

	def __iter__(self):
		self.current = 0
		return self

	def __next__(self):
		if self.current < len(self._fields):
			name = self._fields[self.current]
			self.current += 1
			return name, getattr(self, name)
		else:
			raise StopIteration

p = Parameter(setting)

