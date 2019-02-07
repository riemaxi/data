#!/usr/bin/env python3

import os

pid = open('process.pid').read().strip()
os.system('kill {}'.format(pid))

os.system('rm -f process.pid')
