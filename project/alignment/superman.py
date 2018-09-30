import math

class Superman:
	def __init__(self, match_score = 2, mismatch_score = -1, indel_score = -1):
		self.match_score = match_score
		self.mismatch_score = mismatch_score
		self.indel_score = indel_score
		
	def equals(self, a,b, epsilon=1.0):
		return abs(a-b) <= epsilon
		
	def match_bonus(self, a,b):
		return math.exp(-abs(a-b))
		
	def score(self, a,b, epsilon = 1.0):
		return self.match_score * self.match_bonus(a,b) * self.equals(a,b,epsilon) or self.mismatch_score
		
	def numbers(self, a,b, agaps, bgaps, epsilon=1.0):
		pass
		
	def align(aseq,bseq,epsilon=1.0):
		pass
		
	#tools
	def deploy(seq, gaps):
		pass
		
		