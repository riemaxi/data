import sys
from parameter import p

def next_window(size):
	w = ''
	while size>0:
		c = sys.stdin.read(1)
		if c:
			w += c
			size -= 1			
		else:
			break
		
	return w

def first_reduction(w):
	return w.count('1'), w[int(len(w)/2):].count('1') 
	
def next_reduction(w, overlap):
	ff = w.count('1')
	return ff + overlap, ff
	
wsize = int(p.size)
step = wsize/2

w = next_window(wsize)
ff, overlap = first_reduction(w)
print(ff)

while w:
	ff, overlap = next_reduction(w, overlap)
	print(ff)
		
	w = next_window(step)