#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from pprint import pprint as p_
from random import choice, random, shuffle
from egg import *


R = dict((name, ((),)) for name in ascii_lowercase)


K = list(ascii_lowercase)
shuffle(K)

P = {}
for k, v in zip(ascii_lowercase, K):
  if random() < 0.25:
    v = v,
  P[k] = v
  print k, ':', v
print


print ascii_lowercase,
# Run until the system returns to a previously seen state.
detect_cycle(R, P)

#print
#run_n_cycles(R, P, 20)
