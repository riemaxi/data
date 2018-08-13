import needle
import sys

a = [float(f) for f in open(sys.argv[1]).read().strip().split('\n')]
b = [float(f) for f in open(sys.argv[2]).read().strip().split('\n')]


identity, score, align1, symbol, align2 = needle.align(a,b)

print(identity)
print(*align1, sep = '\t')
print(*align2, sep = '\t')

