#!/usr/bin/env python3

import sys

sep = ','
path = sys.argv[1]

def load(path, sep):
	data = {}
	for record in  open(path):
		record = record.strip().split(sep)

		data[record[0]] = record[1:]

	return data

def discern_features(clsa, clsb, feature, data):
	return [i for i in feature if data[clsa][i] != data[clsb][i]]

feature = [int(s) for s in sys.argv[2].split(',')]
data = load(path, sep)

for line in sys.stdin:
	line = line.strip().split('\t')

	df = discern_features(line[1], line[4], feature, data)
	print(line[1], line[4], ','.join([str(i) for i in df]), sep = '\t')
