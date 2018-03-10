#!/usr/bin/env python3

import syslog

for i in range(100):
	syslog.syslog('message {}'.format(i))
