#!/usr/bin/env python3

import os

os.system('rm -f process.pid')

os.system('./lookup.py&')
