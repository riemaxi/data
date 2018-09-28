
import math

class Hellberg:
	def __init__(self, scales, normfactor):
		self.scales = {}
		for aa,z1,z2,z3 in [entry.split('\t') for entry in scales.split('\n')]:
			self.scales[aa] = float(z1),float(z2),float(z3)
		self.p = normfactor
		
	def ac(self, sequence, z, lag):
		n = len(sequence)
		s = sum([self.scales[sequence[i]][z] * self.scales[sequence[i+lag]][z] for i in range(n-lag)])
		return s/math.pow(n-lag, self.p)
	
	

	def cc(sequence, za,zb, lag):
		n = len(sequence)
		s = sum([self.scales[sequence[i]][za] * self.scales[sequence[i+lag]][zb] for i in range(n-lag)])
		return s/math.pow(n-lag, self.p)

