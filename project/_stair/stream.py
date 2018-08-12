import sys

c = sys.stdin.read(1)	
while c:
		print('{:b}'.format(int(c,16)), end = '')
		c = sys.stdin.read(1)
