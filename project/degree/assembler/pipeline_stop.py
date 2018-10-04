#!/usr/bin/env python3

from signal import SIGTERM
import os
from parameter import *

try:
	id = int(open('log/pipeline.pid').read().strip())
	os.kill(id, SIGTERM)
except OSError as e:
	print(e)

os.system('rm -f log/pipeline*')
