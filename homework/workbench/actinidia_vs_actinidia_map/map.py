#!/usr/bin/env python3

import sys
import clearwater as cw

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
count = int(sys.argv[4])

mapper = cw.Warmmapper()

def mapqueries(count, mapper):
	with open(report,'w') as file:
		for line in open(reference):
			ri, r = line.strip().split('\t')
			r = string2stairs(r)

			for line in open(query):
				qi, q = line.strip().split('\t')
				q = string2stairs(q)

				print('mapping ...', ri, qi, len(r), len(q), sep = '\t')

				(scr,(rstart,rend),(qstart,qend), cnt),_ = mapper.map(r,q)

				record = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(ri, qi, cnt, rstart, rend, qstart, qend, '{:0.5f}'.format(scr))
				file.write(record)


				count -= 1

				if not count:
					return

def mapcontrols(mapper):
	with open(report,'a') as file:
		id, data = next(open(reference)).strip().split('\t')

		data = string2stairs(data)

		ci = id
		for i in range(10):
			c = data[i:i-10]

			print('mapping control ...', id, ci, len(data), len(c), sep = '\t')

			(scr,(rstart,rend),(qstart,qend), cnt),_ = mapper.map(data,c)

			record = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(id, ci, cnt, rstart, rend, qstart, qend, '{:0.5f}'.format(scr))
			file.write(record)


mapqueries(count, mapper)
mapcontrols(mapper)
