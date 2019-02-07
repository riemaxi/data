#!/usr/bin/env python3

import os
from parameter import p

os.system('rm -f process.pid')

os.system('./sample.py | ./scatter.py&')
