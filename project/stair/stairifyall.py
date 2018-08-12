import os

paths = [entry.split('\t')[0] for entry in open('data/index.dat').read().split('\n')]

for path in paths:
	os.system('stairify.bat data\{0}'.format(path))