# This software has been writen by Samuel Ferrer
# ferraxi@gmail.com
# copyright © 2018

ZERO = '0'
ONE = '1'

def wrap(data, size):
	for i in range(0, len(data), size):
		yield data[i:i+size]


def replace(s, zero):
	return ''.join([ZERO if a in zero else ONE for a in s])

# The transformation itself
def pack(data, zero):
	lst = list(wrap(data,4))

	lst = ['{:<04}'.format(replace(s,zero)) for s in lst]

	return ''.join(['{:X}'.format(int(a,2)) for a in lst])


# Asynchronic version of transform for very large  sequences
def atransform(id, datasize, data, zero, sink):
	sink.head(id, datasize)
	sink.tail(pack(data.upper(),zero))
	sink.end()

# Binn the DNA sequence
# parameters
# data - the DNA sequence to be binned
# zero - the letters to be converted to zero, the rest of the letters will be converted to one
def transform(data, zero):
	return pack(data.upper(),zero)


# Complement of a sequence
# parameters
# data - the DNA sequence
def complement(data):
	CMP = {'A': 'T', 'T' : 'A', 'C' : 'G', 'G' : 'C' ,'N' : 'N'}
	return ''.join([CMP[b] for b in data[::-1]])

# Binn the complementary sequence
# parameters
# data - the DNA sequence to be binned
# zero - the letters to be converted to zero, the rest of the letters will be converted to one
def complement_transform(data, zero):
	return pack(complement(data.upper()),zero)

