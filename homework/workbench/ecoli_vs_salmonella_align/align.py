#!/usr/bin/env python3

import sys
import cleanneedle as cn

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference_path = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
maxcount = int(sys.argv[4])
maxgroups = 4

top = 5
maxscore = .3

al = cn.Aligner(cn.Setting(match_factor = 4))

def alignqueries(maxcount, al):
	reference = open(reference_path)
	with open(report,'w', buffering = 1) as file:

		groups = maxgroups
		for line in reference:
			ri, r = line.strip().split('\t')

			count = maxcount
			for line in open(query):
				qi, q = line.strip().split('\t')

				print('aligning ...', ri, qi, len(r), len(q), sep = '\t')

				for dr, dq, score in cn.Tool.topalignments(al.deployments(string2stairs(r), string2stairs(q), first = False), maxscore, top):

					score = '{:0.4f}'.format(score) 
					file.write( '{}\t{}\n{}\n{}\n{}\n\n'.format( ri,qi, dr, dq, score) )

					print(ri, qi, score , flush = True, sep='\t')

					count -= 1
					if not count:
						groups -= 1
						if not groups:
							return
						else:
							break

def aligncontrols(al):
	with open(report,'a', buffering = 1) as file:
		id, data = next(open(reference_path)).strip().split('\t')

		data = string2stairs(data)

		ci = id
		for i in range(10):
			c = data[i:i-10]

			print('aligning control ...', id, ci, len(data), len(c), sep = '\t')

			for dr, dq, score in cn.Tool.topalignments(al.deployments(data, c, first = False), maxscore, top):

				score = '{:0.2f}'.format(score)
				file.write( '{}\t{}\n{}\n{}\n{}\n\n'.format( id,ci, dr, dq, score ) )

				print(id, ci, score , flush = True, sep='\t')


alignqueries(maxcount, al)
aligncontrols(al)
