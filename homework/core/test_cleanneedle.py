#!/usr/bin/env python3

import cleanneedle as cn

a = [45,56,34,67,89,88,84,76,56,55,54,45,44,43,32,23,45,67,78]
b = [45,56,34,67,89,88,84,76,56,55,54,         32,23,45,67,78]
c = [45,56,34,      88,84,76,56,55,54,45,44,            67,78]
d = [45,56,34,      88,84,76,56,55,54,45,44                  ]
e = [               88,84,76,56,55,54,45,44,            67,78]

print('testing deploy...')
print(*cn.Tool.deploy(a, {}, symbol='--'))
print(*cn.Tool.deploy(b, {11:3}, symbol='--'))
print(*cn.Tool.deploy(c, {3:2,11:4}, symbol='--'))
print(*cn.Tool.deploy(d, {3:2,11:6}, symbol='--'))
print(*cn.Tool.deploy(e, {0:5,11:4}, symbol='--'))

print('\ntesting totalscore')
d = cn.Tool.deploy(d, {3:2,11:6}, symbol='-')
e = cn.Tool.deploy(e, {0:5,11:4}, symbol='-')

print(cn.Aligner().totalscore(d,e))
a = cn.Tool.deploy(a, {}, symbol='-')
b = cn.Tool.deploy(b, {11:3}, symbol='-')
print(cn.Aligner().totalscore(a,b))



