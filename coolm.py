#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from pprint import pprint as p_
from random import choice, random, shuffle, sample
from egg import *


ops = and_, or_, nand, nor, xor


R = dict((name, ((),)) for name in ascii_lowercase)


K = list(ascii_lowercase)
shuffle(K)

P = {}
for ch in ascii_lowercase:
  if random() > 0.5:
    P[ch] = nor(ch, K.pop())
  else:
    P[ch] = K.pop()


#R['a'] = ()
p_(P)
print


print ascii_lowercase,
# Run until the system returns to a previously seen state.
detect_cycle(R, P)

#print
#run_n_cycles(R, P, 20)