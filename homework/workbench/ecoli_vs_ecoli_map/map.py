#!/usr/bin/env python3

import sys
import clearwater as cw

def string2stairs(seq, sep = ' '):
	return [float(s) for s in seq.split(sep)]

reference_path = sys.argv[1]
query = sys.argv[2]
report = sys.argv[3]
groupcount = int(sys.argv[4])

maxgroups = 30

reference = open(reference_path)

mapper = cw.Warmmapper()

def mapqueries(groupcount, mapper):
	with open(report,'w') as file:
		groups = maxgroups
		for line in reference:
			ri, r = line.strip().split('\t')
			r = string2stairs(r)
			count = groupcount

			for line in open(query):
				qi, q = line.strip().split('\t')
				q = string2stairs(q)

				print('mapping ...', maxgroups - groups, groupcount - count, len(r), len(q), sep = '\t')

				(scr,(rstart,rend),(qstart,qend), cnt),_ = mapper.map(r,q)

				record = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(maxgroups - groups, groupcount - count, cnt, rstart, rend, qstart, qend, '{:0.5f}'.format(scr))
				file.write(record)


				count -= 1

				if not count:
					groups -= 1
					if not groups:
						return
					else:
						break

def mapcontrols(groupcount, mapper):
	with open(report,'a') as file, open(reference_path) as rfile:
		_, data1 = next(rfile).strip().split('\t')
		_, data2 = next(rfile).strip().split('\t')

		data = string2stairs(data1) + string2stairs(data2)[len(data1)//2:]

		id = maxgroups
		for i in range(2):
			c = data[i:i-2]

			print('mapping control ...', id, groupcount + i, len(data), len(c), sep = '\t')

			(scr,(rstart,rend),(qstart,qend), cnt),_ = mapper.map(data,c)

			record = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(id, groupcount + i, cnt, rstart, rend, qstart, qend, '{:0.5f}'.format(scr))
			file.write(record)


mapqueries(groupcount, mapper)
mapcontrols(groupcount, mapper)
