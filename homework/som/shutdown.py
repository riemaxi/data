#!/usr/bin/env python3

import os

for line in open('process.pid'):
	pid = line.strip()
	os.system('kill {}'.format(pid))

os.system('rm -f process.pid')
os.system('rm -f log/*')
