#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import ascii_lowercase
from itertools import product
from egg import xor, and_, or_
from machine import Machine, _, o, view_program


def FBA(a, b, c):
  '''Full Bit Adder.'''
  k = xor(a, b)
  return xor(k, c), or_(and_(k, c), and_(a, b))


def make_adder(reg0, reg1):
  if len(reg0) != len(reg1): raise ValueError
  bits, carry = [], _
  for r0, r1 in zip(reg0, reg1):
    sum_bit, carry = FBA(r0, r1, carry)
    bits.append(sum_bit)
  return bits, carry


a, b, c, x, y, z = 'abcxyz'
reg0, reg1 = (a, b, c), (z, y, x)
sum_bits, carry = make_adder(reg0, reg1)
program = dict(zip(reg0, sum_bits))
program['o'] = carry
#print view_program(program)
m = Machine(ascii_lowercase, program)


B = _, o
for m.R[x], m.R[y], m.R[z] in product(B, B, B):
  m.R[a] = m.R[b] = m.R[c] = m.R['o'] = _
  print '    ', ascii_lowercase
  n, looped_to, seen = m.find_cycle(noisy=True)
