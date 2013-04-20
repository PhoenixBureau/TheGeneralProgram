# -*- coding: utf-8 -*-
from egg import xor, Reduce, solve, s, fstan, nor


op = xor


E = op('a', 'z')
for _ in range(7):
  E = fstan(E)
  print s(E)
  E = (op(E, 'z'))
