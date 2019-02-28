#!/usr/bin/env python3

import random
import ml

ann = ml.ANN( ml.Tool.read_network('data/network.1') )

#print(*ann.layer(0), sep='\n')
#print(*ann.links(0,0), sep='\n')

#print( ann.terminals(ann.layer(1)))

for i in range(5):
	output = ann.output( [random.random(),random.random(),random.random()] )
	print( ann.test(output) )

#print(ml.Tool.network2string(ml.Tool.initialize()))
