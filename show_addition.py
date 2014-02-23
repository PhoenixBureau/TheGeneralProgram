#!/usr/bin/env python
from string import ascii_lowercase
from itertools import product
from machine import (
  Machine, _, o, view_program,
  flipflop, make_adder, make_switch,
  )


a, b, c, d, w, x, y, z = 'abcdwxyz'
oh, p, q, r, s, t = 'opqrst'
reg0, reg1 = (a, b, c, d), (z, y, x, w)
R, X, A = (r, s, t), (x, y, z), (a, b, c)


program = {}
sum_bits, program[oh] = make_adder(reg0, reg1)
program.update(zip(reg0, sum_bits))
program.update(zip(R, make_switch(p, X, A)))
program[p] = flipflop(p, c, oh)


print view_program(program)
m = Machine(ascii_lowercase, program)


B = _, o
for m.R[w], m.R[x], m.R[y], m.R[z] in product(B, B, B, B):
  print '    ', ascii_lowercase, m.as_int()
  n, looped_to, seen = m.find_cycle(noisy=True)
  m.reset()
