#!/usr/bin/env python3

import os

for line in open('process.pid'):
	os.system('kill {}'.format(line.strip()))

os.system('rm -f process.pid')
