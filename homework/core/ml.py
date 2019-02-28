import math
import random

class Tool:
	def read_network(path):
		with open(path) as file:
			data = [ [float(v) for v in next(file).strip().split('\t')] ]

			for line in file:
				a,b,l,w = line.strip().split('\t')
				data +=[(int(a),int(b),int(l),float(w))]
		return data

	def initialize( layer = [2,3,2], target = (1.0,3.0)):
		topology = [target]

		for l in range(len(layer)-1):
			for k in range(layer[l]):
				for m in range(layer[l+1]):
					topology += [(k,m,l, random.random())]

		return topology

	def network2string(topo,target_template='{:0.2f}',  template='{}\t{}\t{}\t{:0.2f}'):
		return '\t'.join([target_template.format(f) for f in topo[0]]) + '\n' + '\n'.join([template.format(a,b,l,w) for a,b,l,w in topo[1:]])


class ANN:
	def  __init__(self, weights = []):
		self.target = weights[0]
		self.weights = weights[1:]

		self.layers = max([cl for  _,_,cl,_ in self.weights]) + 1

	def filter(self, s):
		return 1/(1 + math.exp(-s))

	def layer(self, i):
		return [(a,b,w) for a,b,l,w in self.weights if l == i]


	def terminals(self, layer):
		return { b for _,b,_ in layer }


	def links(self, l):
		layer = self.layer(l)
		for i in self.terminals(layer):
			yield [(a,w) for a,b,w in layer if b==i]

	def feedforward(self, l, input):
		output = []
		for link in self.links(l):
			output += [self.filter(sum( [w*input[a] for a,w in link]  ) )]
		return output


	def output(self, input):
		output = input
		for l in range(self.layers):
			output = self.feedforward(l, output )

		return output

	def update(self, input):
		output = self.output()
		pass

	def loss(self, v):
		return sum([.5 * (v[i]-self.target[i])**2  for i in range(len(self.target))])

	def test(self, input, epsilon = 0.1):
		output = self.output(input)

		return self.loss(output) <= epsilon
