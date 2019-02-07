#!/usr/bin/env python3

import os
from parameter import p

pid = open('process.pid').read().strip()
os.system('kill {}'.format(pid))

os.system('rm -f process.pid')
os.system('rm -f {}'.format(p.report_path))
