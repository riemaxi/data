#!/usr/bin/env python3

from parameter import p

print('profession', p.profession, sep = '----')
for name, value in p:
	print(name, value, sep = ' = ')
