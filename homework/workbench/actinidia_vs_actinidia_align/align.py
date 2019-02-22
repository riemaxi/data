#!/usr/bin/env python3

import sys
import cleanneedle as cn

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
count = int(sys.argv[4])

al = cn.Aligner()

def alignqueries(count, al):

	with open(report,'w', buffering = 1) as file:
		for line in open(reference):
			ri, r = line.strip().split('\t')

			for line in open(query):
				qi, q = line.strip().split('\t')

				print('aligning ...', ri, qi, len(r), len(q), sep = '\t')

				for dr, dq, score in cn.Tool.topalignments(al.deployments(string2stairs(r), string2stairs(q)), maxscore = 0.0):

					score = '{:0.2f}'.format(score) 
					file.write( '{}\t{}\n{}\n{}\n{}\n\n'.format( ri,qi, dr, dq, score) )

					print(ri, qi, score , flush = True, sep='\t')

def aligncontrols(al):
	with open(report,'a', buffering = 1) as file:
		id, data = next(open(reference)).strip().split('\t')

		data = string2stairs(data)

		ci = id
		for i in range(10):
			c = data[i:i-10]

			print('aligning control ...', id, ci, len(data), len(c), sep = '\t')

			for dr, dq, score in cn.Tool.topalignments(al.deployments(data, c), maxscore = 0.0):

				score = '{:0.2f}'.format(score)
				file.write( '{}\t{}\n{}\n{}\n{}\n\n'.format( id,ci, dr, dq, score ) )

				print(id, ci, score , flush = True, sep='\t')


alignqueries(count, al)
aligncontrols(al)
