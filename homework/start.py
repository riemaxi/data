#!/usr/bin/env python3

import os

os.system('mkdir -p log')
os.system('rm -f process.pid')

os.system('./lookup.py&')
os.system('./organize.py&')
os.system('./sample.py | ./scatter.py&')

