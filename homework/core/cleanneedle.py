import math

class Tool:
	def alignment2string(data, template = '{:0.2f}', sep=' '):
		return sep.join([template.format(f) if type(f) in (float,int) else f for f in data])

	def deploy(data, gaps, symbol='-'):
		offset = 0
		for i in sorted(gaps):
			data = data[:i + offset] + [symbol]*gaps[i] + data[i + offset:]
			offset += gaps[i]

		return data

	def deploys(data, gaps,template='{:0.2f}', symbol='_____', sep=' '):
		return sep.join([template.format(f) if type(f) in (float,int) else f for f in Tool.deploy(data, gaps, symbol)])


	def deployalignment(a, gapsa, b, gapsb, template='{:0.2f}',  symbol='_____', sep=' '):
		a = Tool.deploy(a, gapsa,symbol)
		b = Tool.deploy(b, gapsb,symbol)
		tail = len(a) - len(b)
		if tail>0:
			return  Tool.alignment2string(a,template,sep), Tool.alignment2string(b + [symbol]*tail,template,sep)
		elif tail<0:
			return  Tool.alignment2string(a +  + [symbol]*(-tail),template,sep), Tool.alignment2string(b,template,sep)
		else:
			return  Tool.alignment2string(a,template,sep), Tool.alignment2string(b,template,sep)


	def addgaps(gaps, i, number=1):
		prevgap = gaps.get(i+1,0)
		if prevgap:
			gaps[i] = prevgap + number
			del gaps[i+1]
		else:
			gaps[i] = gaps.get(i,0) + number

		return Tool.copygaps(gaps)

	def lpadgaps(gaps, number = 1):
		return Tool.addgaps(gaps, 0, number) if gaps.get(0) else gaps


	def printmatrix(m, sep='\t'):
		rows, cols, minrow, mincol = m.dimension()

		print('', end=sep)
		for col in range(mincol, mincol + cols):
			print(col, end=sep)

		print()

		for row in range(minrow, minrow + rows):
			print(row, end=sep)
			for col in range(mincol, mincol + cols):
				print(m.get(row, col), end=sep)
			print()


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

	def limits(self):
		minrow, mincol = float('inf'), float('inf')
		maxrow, maxcol = float('-inf'), float('-inf')
		for row, col in self.data:
			minrow, mincol = min(row, minrow), min(col, mincol)
			maxrow, maxcol = max(row, maxrow), max(col, maxcol)

		return minrow, maxrow, mincol, maxcol

	def dimension(self):
		minrow, maxrow, mincol, maxcol = self.limits()

		if len(self.data):
			return maxrow - minrow + 1, maxcol - mincol + 1, minrow, mincol
		else:
			return 0,0,0,0


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

		for row in range(rows):
			m.set(row,0, (row+1) * self.mismatch_penalty)
		for col in range(cols):
			m.set(0, col, (col+1) * self.mismatch_penalty)

		m.set(-1,-1,0)

		return m

	def setmatrix(self,seqa,seqb):
		matrix = self.initmatrix(len(seqa), len(seqb))
		for row in range(len(seqa)):
			for col in range(len(seqb)):
				a,b = seqa[row], seqb[col]

				matrix.set(row,col,max(	matrix.get(row-1,col-1) + self.score(a,b),
							matrix.get(row-1,col) + self.gap_penalty,
							matrix.get(row,col-1) + self.gap_penalty)
						)


		return matrix


	def gaps(self, matrix, seqa, seqb, stack):
		while len(stack):
			gapsa, gapsb, row, col = stack.pop()

			if row >= 0 and col >= 0:
				uscore, lscore, dscore = matrix.get(row-1,col), matrix.get(row, col-1), matrix.get(row-1,col-1)
				maxscore = max(uscore, lscore, dscore)

				if dscore == maxscore:
					stack += [(Tool.copygaps(gapsa), Tool.copygaps(gapsb), row-1, col-1)]

				if uscore == maxscore:
					stack += [(Tool.copygaps(gapsa), Tool.addgaps(gapsb,col), row-1,col)]


				if lscore == maxscore:
					stack += [(Tool.addgaps(gapsa,row),Tool.copygaps(gapsb), row, col-1)]
			else:
				yield  Tool.lpadgaps(gapsa), Tool.lpadgaps(gapsb)


	def align(self, seqa, seqb):
		matrix = self.setmatrix(seqa, seqb)

		return self.gaps(matrix, seqa, seqb, [({},{}, len(seqa)-1, len(seqb)-1)])

	def totalscore(self, seqa, seqb, gapsymbol = '-', gapscore = 0.5):
		score = 0.0
		for i in range(min(len(seqa), len(seqb))):
			a,b = seqa[i], seqb[i]
			if a != gapsymbol and b != gapsymbol:
				score += [0.0,1.0][self.equals(a,b)]
			else:
				score += gapscore

		return score/len(seqa)
