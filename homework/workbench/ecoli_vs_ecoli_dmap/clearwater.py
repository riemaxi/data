# This software has been writen by Samuel Ferrer
# ferraxi@gmail.com
# copyright © 2018

import math

class Tool:

	def printmatrix(m, seqa, seqb):
		print(' ','\t'.join(['{}'.format(f) for f in seqb]), sep='\t')
		for row in range(len(seqa)):
			print('{}'.format(seqa[row]), end='\t')
			for col in range(len(seqb)):
				print('{:0.2f}'.format(m.get(row,col)), end='\t')
			print()

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


class Setting:
	def __init__(self, match_factor = 0.3, match_threshold = 0.5, gap_penalty = -5.0, mismatch_penalty = -5.0, match_reward = 10.0):
		self.match_factor = match_factor
		self.match_threshold = match_threshold

		self.gap_penalty = gap_penalty
		self.mismatch_penalty = mismatch_penalty
		self.match_reward = match_reward

class Warmmapper:
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


	def setmatrix(self,seqa,seqb):
		matrix = Matrix(-1,-1, len(seqa)-1, len(seqb)-1)
		maxscore, maxpos = float('-inf'), None
		gapping = 1
		for col in range(len(seqb)):
			for row in range(len(seqa)):
				a,b = seqa[row], seqb[col]

				(score, gap)  = max( [	(matrix.get(row-1,col-1) + self.score(a,b),0),
							(matrix.get(row-1,col) + gapping * self.gap_penalty,1),
							(matrix.get(row,col-1) + gapping * self.gap_penalty,1),
							(0,0)
						] )

				matrix.set(row, col, score)
				if score > maxscore:
					maxscore, maxpos = score, (row, col)

				gapping  = gapping + 1 if gap else 1


		return matrix, maxscore, maxpos


	def totalscore(self, matrix, seqa, seqb, maxpos):
		row, col = maxpos
		enda, endb = row, col
		score = 0
		count = 0
		while matrix.get(row,col):
			di = self.distance(seqa[row], seqb[col])
			score = score + di + self.match_threshold

			_, (dr,dc) = max( [	( matrix.get(row-1, col-1),(-1,-1) ),
						( matrix.get(row, col-1),(0,-1) ),
						( matrix.get(row-1, col),(-1,0) )
					] )

			row, col = row + dr, col + dc

			count += 1

		return score, (max(row,0), enda) , (max(col,0),endb) , count


	def map(self, seqa, seqb):
		matrix, _, maxpos = self.setmatrix(seqa, seqb)

		return self.totalscore(matrix, seqa, seqb, maxpos), matrix

