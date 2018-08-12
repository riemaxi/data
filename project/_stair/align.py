import needle

a = [1,2,3,5,6]
b = [1,2,3,5.9]

identity, score, align1, symbol, align2 = needle.align(a,b)

print(identity, score)
print(align1)
#print(symbol)
print(align2)

