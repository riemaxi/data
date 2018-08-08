import sys

index = []
for line in sys.stdin:
	index.append( int(line.strip().split()[0]) )

print(*sorted(index), sep='\n')