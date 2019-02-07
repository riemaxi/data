# This software has been writen by Samuel Ferrer
# ferraxi@gmail.com
# copyright © 2018

def window(data, realsize, wsize,start,q):
	size = len(data)

	if start>=size-1:
		return None,None,None

	for i in range(start, size-1):
		q += '{:>04b}'.format(int(data[i],16))

		if len(q)>=wsize:
			return q[:wsize], q[wsize:],i+1

	if realsize % 4:
		q += '{:>04b}'.format(int(data[start-1],16))[:realsize % 4]
	else:
		q += '{:>04b}'.format(int(data[start-1],16))

	return q,'',size-1

# A first reduction is made at the beginning of the sequence
def first_reduction(w):
	return [w.count('1'), w[int(len(w)/2):].count('1'),w,w] if w else [0,0,None,None]

# The aggregate function
# parameters
# w - the next window in the sequence 
#  overlap - the frequency left from the previous window
def reduction(w, overlap):
	if w:
		ff = w.count('1')
		return [ff + overlap, ff, w]
	else:
		return [0,0,None]

# Transform a binned sequence into a stairs vector
# parameters
# seqsize - the size of the sequence
# wsize - the window size
# data - the binned version of the DNA sequence 
def transform(seqsize, wsize, data, base=100):
	step = wsize//2

	w, qrest, start = window(data,seqsize,wsize,0,'')
	ff, overlap, w, fw = first_reduction(w)

	vector = []
	while w:
		vector += [ff*base/wsize]

		w, rest, start = window(data,seqsize,step, start,qrest)
		ff, overlap, w = reduction(w, overlap)

	return vector

def complement(data, base=100):
	return [base-f for f in data[::-1]]

def complement_transform(seqsize, wsize, data, base=100):
	return complement(transform(seqsize, wsize, data,base), base)

