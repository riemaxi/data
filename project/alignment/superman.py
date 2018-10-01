import math
import queue

GAP = '-'

class Littleman:
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

	def numbers(self, a,b, agaps, bgaps, epsilon = 1.0):
		pass

	def solution(self,aseq,bseq, grid, c,r):
		a,b = [],[]
		while r > 0 and c > 0:
			if grid[r-1][c-1] > max(grid[r][c-1], grid[r-1][c]):
				a = [aseq[c-2]] + a
				b = [bseq[r-2]] + b
				r -= 1
				c -= 1
			else:
				if grid[r-1][c] > max(grid[r-1][c-1], grid[r][c-1]):
					a = [GAP] + a
					b = [bseq[r-2]] + b
					r -= 1
				else:
					a = [aseq[c-2]] + a
					b = [GAP] + b
					c -= 1

		yield a[1:],b[1:]

	def alignment(self,aseq,bseq,epsilon = 1.0):
		cols = len(aseq) + 1
		rows = len(bseq) + 1

		grid = [[0 for x in range(cols+1)] for y in range(rows+1) ]

		for i in range(len(grid[0])):
			grid[0][i] = -i

		for i in range(len(grid)):
			grid[i][0] = -i

		#score aupdate - core of the algorithm
		for r in range(1,rows):
			for c in range(1,cols):
				grid[r][c] = max( [	grid[r-1][c-1] + self.score(float(bseq[r-1]), float(aseq[c-1])),
							grid[r-1][c] + self.indel_score,
							grid[r][c-1] + self.indel_score] )

		return self.solution(aseq,bseq,grid,cols,rows)

class Superman(Littleman):

	def solution(self,aseq,bseq, grid, cols, rows):
		q = queue.Queue()
		q.put((cols, rows, [],[]))

		while not q.empty():
			c,r,a,b = q.get()
			while r > 0 and c > 0:
				if grid[r-1][c-1] > max(grid[r][c-1], grid[r-1][c]):
					a = [aseq[c-2]] + a
					b = [bseq[r-2]] + b
					r -= 1
					c -= 1
					continue

				if grid[r-1][c] > max(grid[r-1][c-1], grid[r][c-1]):
					a = [GAP] + a
					b = [bseq[r-2]] + b
					r -= 1
					continue

				if grid[r][c-1] > max(grid[r-1][c],grid[r-1][c-1]):
					a = [aseq[c-2]] + a
					b = [GAP] + b
					c -= 1
					continue

				if grid[r-1][c-1] == grid[r-1][c]:
					q.put((r-1,c,[aseq[c-2]] + a, [bseq[r-2]] + b))
					q.put((r-1,c-1,[aseq[c-2]] + a, [bseq[r-2]] + b))


				elif grid[r-1][c-1] == grid[r][c-1]:
					q.put((r,c-1,[aseq[c-2]] + a, [bseq[r-2]] + b))
					q.put((r-1,c-1,[aseq[c-2]] + a, [bseq[r-2]] + b))


				elif grid[r][c-1] == grid[r-1][c]:
					q.put((r-1,c,[aseq[c-2]] + a, [bseq[r-2]] + b))
					q.put((r,c-1,[aseq[c-2]] + a, [bseq[r-2]] + b))

				a = [aseq[c-2]] + a
				b = [bseq[r-2]] + b
				r -= 1
				c -= 1

			yield a[1:],b[1:]

	#tools
	def deploy(seq, gaps):
		pass
