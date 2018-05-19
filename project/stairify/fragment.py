#!/usr/bin/env python3
import sys

def read_int_arg(i, dv):
	try:
		return int(sys.argv[i])
	except:
		return dv

def read_char():
	try:
		return sys.stdin.read(1)
	except:
		return ''

def first_fragment(size):
	str = ''
	for i in range(size):
		str += read_char()
	return str

size =  read_int_arg(1, 1000)
number = read_int_arg(2,100)
str = first_fragment(size)

print(str)

c = read_char()
while c != '' and number:
	str = str[1:]
	str += c
	print(str)

	c = read_char()
	number -= 1
