import sys

def stream(s = sys.stdin, sep = '\t'):
	for line in s:
		yield line.strip().split(sep)
