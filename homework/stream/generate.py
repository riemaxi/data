#!/usr/bin/env python3

import random
import sys

def generate():
	return ''.join(['ACGT'[random.randint(0,3)] for _ in range(10000)])

with open(sys.argv[1],'w') as file:
	file.write('{}'.format(generate()))
