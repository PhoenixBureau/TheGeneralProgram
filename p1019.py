from gmm import LilMachine, K

p1019 = {
 'a': 'j',
 'b': 'e',
 'c': ((('c',), ('f',)), ('c', 'f')),
 'd': 'b',
 'e': ((('i',), ('h',)), ('i', 'h')),
 'f': ('i',),
 'g': ((('c',), ('d',)), ('c', 'd')),
 'h': ('c',),
 'i': ((('g',), ('b',)), ('g', 'b')),
 'j': ((('i',), ('a',)), ('i', 'a'))}

lm = LilMachine(K, **p1019)

for n in lm:
  print n
print lm
