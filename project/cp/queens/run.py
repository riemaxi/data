
import os
import sys

start = int(sys.argv[1])
step = int(sys.argv[2])
startsize = int(sys.argv[3])
number = int(sys.argv[4])
runs = int(sys.argv[5])

for i in range(start,number):
	for j in range(runs):
		os.system('model -time 60000 {}'.format(startsize + step*i))
