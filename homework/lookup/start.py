#!/usr/bin/env python3

import os
from parameter import p

os.system('rm -f process.pid')

for port in p.ports.split(','):
	os.system('./lookup.py {}&'.format(port))
