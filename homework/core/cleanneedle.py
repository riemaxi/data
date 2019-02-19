import math

class Tool:
	def deploy(data, gaps, symbol='-'):
		offset = 0
		for i in sorted(gaps):
			data = data[:i + offset] + [symbol]*gaps[i] + data[i + offset:]
			offset += gaps[i]

		return data

	def addfaps(gaps, i, number=1):
		prevgap = gaps.get(i+1,0)
		if prevgap:
			gaps[i] = prevgap + number
			del gaps[i+1]
		else:
			gaps[i] = gaps.get(i,0) + number


	def copygaps(gaps):
		return gaps.copy()

class Setting:
	def __init__(self, match_factor = 0.3, match_threshold = 0.5, gap_penalty = -1.0, mismatch_penalty = -1.0, match_reward = 1.0):
		self.match_factor = match_factor
		self.match_threshold = match_threshold

		self.gap_penalty = gap_penalty
		self.mismatch_penalty = mismatch_penalty
		self.match_reward = match_reward


class Matrix:
	def __init__(self, defvalue = 0):
		self.defvalue = defvalue
		self.data = {}

	def default(self,row, col):
		return self.defvalue

	def get(self,row, col):
		return self.data.get((row,col), self.default(row, col))

	def set(self, row, col, value):
		self.data[(row,col)] = value


class Aligner:
	def __init__(self, setting = Setting()):
		self.match_factor = setting.match_factor
		self.match_threshold = setting.match_threshold

		self.gap_penalty = setting.gap_penalty
		self.mismatch_penalty = setting.mismatch_penalty
		self.match_reward = setting.match_reward


	def distance(self, a,b):
		return math.exp(-self.match_factor* abs(a - b)) - self.match_threshold

	def equals(self, a,b):
		return self.distance(a,b)>=0

	def score(self, a,b):
		return [self.mismatch_penalty, self.match_reward][self.equals(a,b)]


	def initmatrix(self, rows, cols):
		m = Matrix()

		for row in range(-1,rows):
			m.set(row,0, self.mismatch_penalty)
		for col in range(-1,cols):
			m.set(0, col, self.mismatch_penalty)

		m.set(-1,-1,0)

		return m

	def setmatrix(self,seqa,seqb):
		matrix = self.initmatrix(len(seqa), len(seqb))
		for row in range(len(seqa)):
			for col in range(len(seqb)):
				a,b = seqa[row], seqb[col]

				matrix.set( max(matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty)
						)


		return matrix


	def gaps(self, matrix, seqa, seqb, maxpos, stack):
		while stack:
			gapsa, gapsb, row, col = stack.pop()

			if row >= 0 and col >= 0:
				if matrix.get(row, col) == matrix.get(row-1,col-1) + self.score(row, col):
					stack += [(gapsa, gapsb, row-1, col-1)]
				elif matrix.get(row,col) == matrix.get(row-1,col) + self.gap_penalty:
					stack += [(Tool.copygaps(gapsa), Tool.addgaps(gapsb,col), row-1,col)]
				else:
					stack += [(Tool.addgaps(gapsa,row),Tool.copygaps(gapsb), row, col-1)]
			if row >= 0:
				gapsa = Tool.addgaps(gapsa, row, row + 1)
			if col >= 0:
				gapsb = Tool.addgaps(gapsb, col, col + 1)

			yield  gapsa, gapsb

		return None

	def align(self, seqa, seqb):
		matrix = self.setmatrix(seqa, seqb)

		return self.gaps(matrix, seqa, seqb, [({},{}, len(seqa)-1, len(seqb)-1)])

	def totalscore(self, seqa, seqb, gapsymbol = '-', gapscore = 0.5):
		score = 0.0
		for i in range(len(seqa)):
			a,b = seqa[i], seqb[i]
			if a != gapsymbol and b != gapsymbol:
				score += [0.0,1.0][self.equals(a,b)]
			else:
				score += gapscore

		return score/len(seqa)
