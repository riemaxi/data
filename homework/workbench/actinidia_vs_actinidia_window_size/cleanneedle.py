import math

class Tool:
	def distance(a,b, match_factor = 0.3, match_threshold = 0.5):
		def pwdistance(a,b, match_factor = 0.3, match_threshold = 0.5):
			return math.exp(-match_factor* abs(a - b)) - match_threshold

		def equals(a,b):
			return pwdistance(a,b,match_factor, match_threshold)>=0

		size = min(len(a), len(b))
		return sum([[0,1][equals(a[i],b[i])] for i in range(size)])/size



	def topalignments(list, maxscore = .6, top = 2):
		scores = []
		for da,db,score in list:
			if score >= maxscore and not score in scores:
				scores += [score]
				yield Tool.alignment2string(da),Tool.alignment2string(db),  score

				top -= 1
				if not top:
					break


	def trimalignment(a,b, symbol):
		offset = 0
		while (a[offset], b[offset]) == (symbol,symbol):
			offset += 1

		return a[offset:], b[offset:]

	def alignment2string(data, template = '{:0.2f}', sep=' '):
		return sep.join([template.format(f) if type(f) in (float,int) else f for f in data])

	def deploy(data, gaps, symbol='-'):
		offset = 0
		for i in sorted(gaps):
			data = data[:i + offset] + [symbol]*gaps[i] + data[i + offset:]
			offset += gaps[i]

		return data

	def deploys(data, gaps,template='{:0.2f}', symbol='_____', sep=' '):
		return Tool.alignment2string( Tool.deploy(data, gaps, symbol), template, sep )


	def deployalignments(a, gapsa, b, gapsb, template='{:0.2f}',  symbol='_____', sep=' '):
		a = Tool.deploy(a, gapsa,symbol)
		b = Tool.deploy(b, gapsb,symbol)
		tail = len(a) - len(b)
		if tail>0:
			return  Tool.alignment2string(a,template,sep), Tool.alignment2string(b + [symbol]*tail,template,sep)
		elif tail<0:
			return  Tool.alignment2string(a + [symbol]*(-tail),template,sep), Tool.alignment2string(b,template,sep)
		else:
			return  Tool.alignment2string(a,template,sep), Tool.alignment2string(b,template,sep)

	def deployalignment(a, gapsa, b, gapsb, symbol='_____'):
		a = Tool.deploy(a, gapsa,symbol)
		b = Tool.deploy(b, gapsb,symbol)
		tail = len(a) - len(b)
		if tail>0:
			return  Tool.trimalignment(a, b + [symbol]*tail, symbol)
		elif tail<0:
			return  Tool.trimalignment(a + [symbol]*(-tail), b, symbol)
		else:
			return  Tool.trimalignment(a, b, symbol)



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
	def __init__(self, irow = 0, icol = 0,frow = 0, fcol = 0,  defvalue = 0):
		self.defvalue = defvalue
		self.irow = irow
		self.icol = icol
		self.frow = frow
		self.fcol = fcol

		self.initialize()

	def initialize(self):
		rows, cols,_,_ = self.dimension()
		self.data = [[self.defvalue for _ in range(rows)] for _ in range(cols)]


	def default(self,row, col):
		return self.defvalue

	def get(self,row, col):
		return self.data[col - self.icol][row - self.irow]

	def set(self, row, col, value):
		self.data[col - self.icol][row - self.irow] = value

	def limits(self):
		return self.irow, self.frow, self.icol, self.fcol

	def dimension(self):
		minrow, maxrow, mincol, maxcol = self.limits()
		return maxrow - minrow + 1, maxcol - mincol + 1, minrow, mincol


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
		m = Matrix(-1,-1, rows-1, cols-1)

		for row in range(rows):
			m.set(row,-1, (row+1) * self.mismatch_penalty)
		for col in range(cols):
			m.set(-1, col, (col+1) * self.mismatch_penalty)

		m.set(-1,-1,0)

		return m

	def setmatrix(self,seqa,seqb):
		matrix = self.initmatrix(len(seqa), len(seqb))
		gapping = 1
		for row in range(len(seqa)):
			for col in range(len(seqb)):
				a,b = seqa[row], seqb[col]

				(score, gap) = max(	(matrix.get(row-1,col-1) + self.score(a,b),0),
							(matrix.get(row-1,col) + gapping * self.gap_penalty,1),
							(matrix.get(row,col-1) + gapping * self.gap_penalty,1))

				matrix.set(row,col, score)
				gapping = gapping + 1 if gap else 1

		return matrix


	def allgaps(self, matrix, seqa, seqb, stack):
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
				yield gapsa, gapsb

	def gaps(self, matrix, seqa, seqb):
		gapsa, gapsb = {}, {}
		row, col = len(seqa) - 1, len(seqb) - 1
		if row >= 0 and col >= 0:
			_, (u,l) = max(	(matrix.get(row-1,col), (-1,0)),
					(matrix.get(row, col-1), (0,-1)),
					(matrix.get(row-1,col-1), (-1,-1))
				)

			(row, col) = (row + u, col + l)

			if (u,l) == (0,-1):
				gapsa = Tool.addgaps(gapsa, row)

			if (u,l) == (-1,0):
				gapsb = Tool.addgaps(gapsb, col)

		yield gapsa, gapsb


	def align(self, seqa, seqb, first = True):
		matrix = self.setmatrix(seqa, seqb)

		if first:
			return self.gaps(matrix, seqa, seqb)
		else:
			return self.allgaps(matrix, seqa, seqb, [({},{}, len(seqa)-1, len(seqb)-1)])

	def totalscore(self, a, b, gapsymbol = '-', gapscore = 0.5):
		v = [[0.0,1.0][self.equals(a[i],b[i])] if a[i] != gapsymbol and b[i] != gapsymbol else gapscore for i in range( min( len(a),len(b) ) )]

		return sum(v)/len(v)

	def deployments(self, a,b,first = True, gapsymbol='_____'):
		for gapsa, gapsb in self.align(a,b, first):
			da, db = Tool.deployalignment(a,gapsa,b,gapsb,gapsymbol)
			yield da, db , self.totalscore(da,db,gapsymbol)

