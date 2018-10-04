#!/usr/bin/env python3

import itertools as it
from parameter import *

readspath = p.longreads_binning_dest.format(p.zero)
contigspath = p.contigs_binning_dest.format(p.zero)
longreads_minsize = int(p.longreads_minsize)
contigs_minsize = int(p.contigs_minsize)

for a,b in it.product(open(readspath), open(contigspath)):
	ida,sizea,_ = a.split()
	idb,sizeb,_ = b.split()

	try:
		if int(sizea)>=longreads_minsize and int(sizeb)>=contigs_minsize:
			print(a.strip())
			print(b.strip())
	except:
		break
