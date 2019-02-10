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
	def __init__(self, defvalue = 0):
		self.defvalue = defvalue
		self.data = {}

	def default(self,row, col):
		return self.defvalue

	def get(self,row, col):
		return self.data.get((row,col), self.default(row, col))

	def set(self, row, col, value):
		self.data[(row,col)] = value

class Setting:
	def __init__(self, match_factor = 0.3, match_threshold = 0.5, gap_penalty = -5.0, mismatch_penalty = -5.0, match_reward = 10.0):
		self.match_factor = match_factor
		self.match_threshold = match_threshold

		self.gap_penalty = gap_penalty
		self.mismatch_penalty = mismatch_penalty
		self.match_reward = match_reward

class Coldmapper:
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

	def setinitialmatrix(self, matrix, colstart, rowstart, dwidth, seqa, seqb):
		maxscore, maxpos = float('-inf'), None
		for col in range(colstart, colstart + dwidth):
			for row in range(rowstart, rowstart + dwidth):
				a,b = seqa[row], seqb[col]

				score =  max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
						0 )

				matrix.set(row, col, score)
				if score > maxscore:
					maxscore, maxpos = score, (row, col)
		return maxscore, maxpos

	def setfrontrow(self, matrix, row, start, extent, seqa, seqb, maxscore, maxpos):
		row += extent - 1
		for col in range(start, min(start + extent, len(seqb))):
				a,b = seqa[row], seqb[col]

				score =  max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
						0 )

				matrix.set(row, col, score)
				if score > maxscore:
					maxscore, maxpos = score, (row, col)
		return maxscore, maxpos


	def setfrontcolumn(self, matrix, start, col, extent, seqa, seqb, maxscore, maxpos):
		col += extent - 1
		for row in range(start, start + extent):
				a,b = seqa[row], seqb[col]

				score =  max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
						0 )

				matrix.set(row, col, score)
				if score > maxscore:
					maxscore, maxpos = score, (row, col)
		return maxscore, maxpos



	def setmatrix(self, seqa, seqb, dwidth):
		matrix = Matrix()
		maxscore, maxpos = self.setinitialmatrix(matrix, 0, 0, dwidth, seqa, seqb )

		colstart, rowstart = 1, 1
		while colstart < len(seqb) - dwidth + 1 and rowstart < len(seqa) - dwidth + 1:
				maxscore, maxpos = self.setfrontrow(matrix, rowstart, colstart, dwidth, seqa, seqb, maxscore, maxpos)
				maxscore, maxpos = self.setfrontcolumn(matrix, rowstart,colstart, dwidth, seqa, seqb, maxscore, maxpos)

				colstart += 1
				rowstart += 1

		while colstart < len(seqb) - dwidth + 1:
			maxscore, maxpos = self.setfrontcolumn(matrix, len(seqa) - dwidth, colstart, dwidth, seqa, seqb, maxscore, maxpos)
			colstart += 1

		while rowstart < len(seqa) - dwidth + 1:
			maxscore, maxpos = self.setfrontrow(matrix, rowstart, len(seqb) - dwidth, dwidth, seqa, seqb, maxscore, maxpos)
			rowstart += 1

		return matrix, maxpos


	def totalscore(self, matrix, seqa, seqb, maxpos, threshold = 30.0):
		row, col = maxpos
		score = 0
		while matrix.get(row,col) and score <= threshold:
			di = self.distance(seqa[row], seqb[col])
			score = score + di + self.match_threshold

			_, (dr,dc) = max( [	( matrix.get(row-1, col-1),(-1,-1) ),
						( matrix.get(row, col-1),(0,-1) ),
						( matrix.get(row-1, col),(-1,0) )
					] )

			row, col = row + dr, col + dc

		return score

	def map(self, seqa, seqb, dwidth = 3, threshold = 30.0):
		matrix, maxpos = self.setmatrix(seqa, seqb,dwidth)

		return matrix, self.totalscore(matrix, seqa, seqb, maxpos, threshold), maxpos

class Hotmapper:
	def __init__(self, setting):
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



	def setuppermatrix(self, matrix, dwidth, seqa, seqb, maxscore, maxpos):
		colstart = dwidth
		for row in range(len(seqa)-dwidth):
			for col in range(colstart, len(seqb)):
				a,b = seqa[row], seqb[col]

				score  = max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
					0 )

				matrix.set(row, col, score)

				if score > maxscore:
					maxscore, maxpos = score, (row, col)

			colstart += 1

		return maxscore, maxpos

	def setlowermatrix(self, matrix, dwidth, seqa, seqb, maxscore, maxpos):
		collen = 1
		for row in range(dwidth, len(seqa)):
			for col in range(collen):
				a,b = seqa[row], seqb[col]

				score  = max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
					0 )

				matrix.set(row, col, score)

				if score > maxscore:
					maxscore, maxpos = score, (row, col)

			collen = min(len(seqb) - dwidth, collen + 1)

		return maxscore, maxpos



	def setmatrix(self, seqa, seqb, dwidth, maxscore, maxpos, matrix):
		maxscore, maxpos = self.setuppermatrix(matrix, dwidth, seqa, seqb, maxscore, maxpos)
		_, maxpos = self.setlowermatrix(matrix, dwidth, seqa, seqb, maxscore, maxpos)

		return maxpos

	def totalscore(self, matrix, seqa, seqb, maxpos):
		row, col = maxpos
		enda, endb = row, col
		score = 0
		count = 0
		while matrix.get(row,col):
			di = self.distance(seqa[row], seqb[col])
			score = score + di + self.match_threshold

			_, (dr,dc) = max( [	( matrix.get( (row-1, col-1),0),(-1,-1) ),
						( matrix.get( (row, col-1),0),(0,-1) ),
						( matrix.get( (row-1, col),0),(-1,0) )
					] )

			row, col = row + dr, col + dc

			count += 1

		return score, (max(row,0), enda) , (max(col,0),endb) , count


	def map(self, seqa, seqb,dwidth, maxscore,maxpos, matrix):
		maxpos = self.setmatrix(seqa, seqb, dwidth, maxscore,maxpos, matrix)

		return self.totalscore(matrix, seqa, seqb, maxpos)

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
		matrix = Matrix()
		maxscore, maxpos = float('-inf'), None
		for col in range(len(seqb)):
			for row in range(len(seqa)):
				a,b = seqa[row], seqb[col]

				score  = max(	matrix.get(row-1,col-1) + self.score(a,b),
						matrix.get(row-1,col) + self.gap_penalty,
						matrix.get(row,col-1) + self.gap_penalty,
						0 )

				matrix.set(row, col, score)
				if score > maxscore:
					maxscore, maxpos = score, (row, col)

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

# Obs. Do not use this function, becasue it is based on Coldmapper which is not discrimating as expected
# Mapper encapsulates two mapping classes: Coldmapper andWarmmapper
# main method: map
# Observe that the sequences are stair vectors
# Coldmapper - Discrimation class
# Warmmapper - Smith-Waterman local alignment implementation
class Mapper:
	def __init__(self, setting = Setting()):
		self.setting = setting

	# Maps two sequences. It first uses a "hard" mapping, which discrimates low scoring mappings
	# parameters
	# seqa, seqb - sequences to be mapped
	# threshold - used by Coldmapped to do the discrimation
	# dwidth - used by Coldmapper to do the discrimation
	def map(self, seqa, seqb,threshold = 30.0,  dwidth = 3):
		matrix, score, pos = Coldmapper(self.setting).map(seqa, seqb, dwidth, threshold)

		if score >= threshold:
			return True, Warmmapper(self.setting).map(seqa, seqb)
		else:
			return False, ((score, (-1,-1), (-1,-1), 0), matrix)

