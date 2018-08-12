import sys
from parameter import p

def window(size):
	w = ''
	while size>0:
		c = sys.stdin.read(1)
		if c:
			w += c
			size -= 1			
		else:
			break
		
	return w

def reduction(w, overlap):
	ff = w.count('1')
	return ff + overlap, ff
	
wsize = int(p.size)
step = wsize/2

w = window(step)
overlap = 0
while w:
	ff, overlap = reduction(w, overlap)
	print(ff*100/wsize)
		
	w = window(step)