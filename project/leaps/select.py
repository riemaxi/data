#!/usr/bin/env python3

import sys

from parameter import p
from stream import stream
from selector import startselector, match

sep = '\t'

startselector(p)
for data in stream():
	if match(data):
		print(sep.join(data))
