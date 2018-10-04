import threading
import time
import math
import copy


class Tool:
	GAP = '-'
	
	def score_to_string(score):
		return '\n'.join(['\t'.join(['{:2.0f}'.format(s) for s in row]) for row in score])

	def match_bonus(a,b):
		return math.exp(-abs(a-b))

	def equals(a,b, epsilon):
		return abs(a-b) <= epsilon

	def numbers(seq1, seq2, gaps1,gaps2, size, epsilon=2.0, match_award=10, match_penalty=-5):
		score, identity = 0,0

		gseq1 = Tool.ideploy(seq1, self.pos1, self.size1, gaps1)
		gseq2 = Tool.ideploy(seq2, self.pos2, self.size2, gaps2)

		pair = Tool.nextpair(gseq1, gseq2)
		while pair:
			a,b = pair

			if a==Tool.GAP or b==Tool.GAP:
				score += self.gap_penalty
			else:
				if Tool.equals(a,b,epsilon):
					identity += 1
					score += match_award + Tool.match_bonus(a, b)
				else:
					score += mismatch_penalty

			pair = Tool.nextpair(gseq1, gseq2)


		return (float(identity) / size) * 100, score


	def addgap(gaps,i):
		prevgap = gaps.get(i+1,0)
		if prevgap:
			gaps[i] = prevgap + 1
			del gaps[i+1]
		else:
			gaps[i] = gaps.get(i,0) + 1


	def nextpair(gen1, gen2):
		try:
			a = next(gen1)
		except:
			return None

		try:
			b = next(gen2)
		except:
			return None

		return a,b

	def gaprange(i, gaps):
		try:
			return next((j,n) for j,n in gaps.items() if j<=i and i<j+n)
		except:
			return None

	def deploy(seq, pos, size, gaps, gapsymbol = 	GAP):
		data = []
		q = []
		for i in range(pos, pos + size):
			grange = Tool.gaprange(i, gaps)
			if grange != None:
				data += gapsymbol
				q += [seq[i]]
			else:
				data += q + [seq[i]]
				q = []

		return data


	def ideploy(seq, pos, size, gaps, gapsymbol = GAP):
		q = []
		for i in range(pos, pos + size):
			grange = Tool.gaprange(i, gaps)
			if grange != None:
				yield gapsymbol
				q += [seq[i]]
			else:
				yield from q + [seq[i]]
				q = []


class Aligner:
	def __init__(self,pos1, pos2, size1, size2, epsilon, match_award=10, mismatch_penalty=-5, gap_penalty=-5):
		self.match_award      = match_award
		self.mismatch_penalty = mismatch_penalty
		self.gap_penalty      = gap_penalty # both for opening and extanding

		self.pos1 = pos1
		self.pos2 = pos2
		self.size1 = size1
		self.size2 = size2
		self.epsilon = epsilon

	def zeros(self,shape):
		m = []
		for x in range(shape[0]):
			m.append([])
			for y in range(shape[1]):
				m[-1].append(0)
		return m

	def create_score(self, m,n):
		score = self.zeros((m+1,n+1))
		for i in range(0, m + 1):
			score[i][0] = self.gap_penalty * i
		for j in range(0, n + 1):
			score[0][j] = self.gap_penalty * j

		return score
	

	def init_score(self, seq1, seq2, m,n):
		score = self.create_score(m,n)

		for i in range(1, m + 1):
			for j in range(1, n + 1):
				a,b = seq1[self.pos1 + i - 1], seq2[self.pos2 + j -1]

				match = score[i - 1][j - 1] + self.match_score(a, b, self.epsilon)
				delete = score[i - 1][j] + self.gap_penalty
				insert = score[i][j - 1] + self.gap_penalty
				score[i][j] = max(match, delete, insert)

		return score
            

	def equals(self, a,b, epsilon):
		return type(a) is float and type(b) is float and abs(a-b) <= epsilon

	def match_bonus(self, a,b):
		return math.exp(-abs(a-b))

	def match_score(self,alpha, beta, epsilon):
		if self.equals(alpha,beta, epsilon):
			return self.match_award + self.match_bonus(alpha, beta)
		else:
			return self.mismatch_penalty

	def isgap(self, i, gaps1, gaps2):
		return len([1 for j,n in gaps1 if j<=i and i<=j+n])>0 or len([1 for j,n in gaps2 if j<=i and i<=j+n])>0


	def numbers(self, seq1, seq2, gaps1,gaps2):

		gseq1 = Tool.ideploy(seq1, self.pos1, self.size1, gaps1)
		gseq2 = Tool.ideploy(seq2, self.pos2, self.size2, gaps2)

		pair = Tool.nextpair(gseq1, gseq2)

		count, score, identity = 0,0,0
		while pair:
			a,b = pair

			if a==Tool.GAP or b==Tool.GAP:
				score += self.gap_penalty
			else:
				count += 1
				if self.equals(a,b,self.epsilon):
					identity += 1
					score += self.match_award + self.match_bonus(a, b)
				else:
					score += self.mismatch_penalty

			pair = Tool.nextpair(gseq1, gseq2)


		return (float(identity) / count) * 100 if count > 0 else 0.0, score
        

class Realman(Aligner):

	def solution(self, seq1, seq2, score, m,n):
		gaps1, gaps2 = {},{}
		i,j = m,n 
		while i > 0 and j > 0:
			a,b = seq1[self.pos1 + i -1], seq2[self.pos2 + j -1]

			score_current = score[i][j]
			score_diagonal = score[i-1][j-1]
			score_up = score[i][j-1]
			score_left = score[i-1][j]

			if score_current == score_diagonal + self.match_score(a, b, self.epsilon):
				i -= 1
				j -= 1
			elif score_current == score_left + self.gap_penalty:
				Tool.addgap(gaps2,i-1)
				i -= 1
			elif score_current == score_up + self.gap_penalty:
				Tool.addgap(gaps1,j-1)
				j -= 1

		# Reach the top left cell
		if j>0:
			gaps1[0] = j
		if i>0:
			gaps2[0] = i
			
		
		return gaps1, gaps2

	def align(self, seq1, seq2):
		m,n = self.size1, self.size2

		score = self.init_score(seq1, seq2, m, n)

		gaps1,  gaps2 = self.solution(seq1, seq2, score, m,n)
		
		return self.numbers(seq1, seq2, gaps1,gaps2), gaps1, gaps2

class Realmen(Aligner):

	def solution(self, seq1, seq2, score, stack):
		i,j, gaps1, gaps2 = stack.pop()
		while i > 0 and j > 0:
			a,b = seq1[self.pos1 + i -1], seq2[self.pos2 + j -1]

			score_current = score[i][j]
			score_diagonal = score[i-1][j-1]
			score_up = score[i][j-1]
			score_left = score[i-1][j]
			
			diagonal, left = False, False

			if score_current == score_diagonal + self.match_score(a, b, self.epsilon):
				i -= 1
				j -= 1
				diagonal = True
			
			if score_current == score_left + self.gap_penalty:
				if diagonal:
					cgaps = copy.deepcopy(gaps2)
					Tool.addgap(cgaps,i-1)
					stack += [(i-1,j, copy.deepcopy(gaps1), cgaps)] # put that direction on hold
				else:
					Tool.addgap(gaps2,i-1)
					i -= 1
					left = True
			
			if score_current == score_up + self.gap_penalty:
				if diagonal or left: # put that direction on hold
					cgaps = copy.deepcopy(gaps1)
					Tool.assgap(cgaps, j-1)
					stack += [(i,j-1, cgaps, copy.deepcopy(gaps2))]
				else:
					Tool.addgap(gaps1,j-1)
					j -= 1

		# Reach the top left cell
		if j>0:
			gaps1[0] = j
		if i>0:
			gaps2[0] = i
			
		return gaps1, gaps2
		
	def solutions(self, seq1, seq2, score, m,n):
		stack = [(m,n, {},{})]
		while len(stack):
			yield self.solution(seq1, seq2, score, stack)

	def alignment(self, seq1, seq2):
		m,n = self.size1, self.size2

		score = self.init_score(seq1, seq2, m, n)
		
		for gaps1,  gaps2 in self.solutions(seq1, seq2, score, m,n):
			yield self.numbers(seq1, seq2, gaps1,gaps2), gaps1, gaps2

		
class Realwater(Aligner):
	def align(self,seq1, seq2):
		m, n = self.size1, self.size2

		# Generate DP table and traceback path pointer matrix
		score = self.zeros((m+1, n+1))      # the DP table
		pointer = self.zeros((m+1, n+1))    # to store the traceback path

		max_score = 0        # initial maximum score in DP table
		# Calculate DP table and mark pointers
		for i in range(1, m + 1):
			for j in range(1, n + 1):
				a,b = seq1[self.pos1 + i - 1], seq2[self.pos2 + j -1]

				score_diagonal = score[i-1][j-1] + self.match_score(a, b, self.epsilon)
				score_up = score[i][j-1] + self.gap_penalty
				score_left = score[i-1][j] + self.gap_penalty
				score[i][j] = max(0,score_left, score_up, score_diagonal)
				if score[i][j] == 0:
					pointer[i][j] = 0 # 0 means end of the path
				if score[i][j] == score_left:
					pointer[i][j] = 1 # 1 means trace up
				if score[i][j] == score_up:
					pointer[i][j] = 2 # 2 means trace left
				if score[i][j] == score_diagonal:
					pointer[i][j] = 3 # 3 means trace diagonal
				if score[i][j] >= max_score:
					max_i = i
					max_j = j
					max_score = score[i][j];

		gaps1, gaps2 = {},{}

		i,j = max_i,max_j    # indices of path starting point

		#traceback, follow pointers
		while pointer[i][j] != 0:
			if pointer[i][j] == 3:
				i -= 1
				j -= 1
			elif pointer[i][j] == 2:
				Tool.addgap(gaps1, j-1)
				j -= 1
			elif pointer[i][j] == 1:
				Tool.addgap(gaps2, i-1)
				i -= 1

		return self.numbers(seq1, seq2, gaps1,gaps2), gaps1, gaps2, j,i


class RealmanProcess(threading.Thread):
	def __init__(self, seq1, seq2, pos1, pos2, size1, size2, epsilon, sink):
		self.seq1 = seq1
		self.seq2 = seq2
		self.epsilon = epsilon
		self.sink = sink

		if pos1 + size1 > len(seq1):
			size1 = len(seq1) - pos1

		if pos2 + size2 > len(seq2):
			size2 = len(seq2) - pos2

		aligner = Realman(pos1, pos2, size1, size2, epsilon)

		threading.Thread.__init__(self)
		self.start()

	def run(self):
		result, gaps1, gaps2 = self.aligner.align(self.seq1, self.seq2)
		sink.handle([self,self.aligner, result, gaps1, gaps2])

class Anchorman:
	def __init__(self, match_award=10, mismatch_penalty=-5, gap_penalty=-5):
		self.match_award      = match_award
		self.mismatch_penalty = mismatch_penalty
		self.gap_penalty      = gap_penalty # both for opening and extanding

		self.pqueue = []

	def handle(self, vector):
		print(process[2:])
		self.pqueue.remove(process[0])


	def align(self, seq1, seq2, epsilon = 5.0, partitions = 100):
		size1, size2 = int(len(seq1)/partitions), int(len(seq2)/partitions)

		lag1, lag2 = int(size1/2), int(size2/2)
		for i in range(int(len(seq1)/size1)):
			ipos = max(0, size1*i - lag1)
			for j in range(int(len(seq2)/size2)):
				self.pqueue.put( RealmanProcess(seq1, seq2, ipos, max(0,size2*j - lag2), size1, size2, epsilon, self) )

		while not self.pqueue.empty():
			time.sleep(1)
