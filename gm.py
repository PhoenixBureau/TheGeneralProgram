#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from egg import *


# Let there be a register of bits.
R = dict((name, ()) for name in ascii_lowercase)


# Let there be a set of expressions denoting transformations to apply
# to bits in the register to develop new bit-values for them.
microcode = {

  ((),): 'a',  # The identity expression.

  (): ('a',),  # The inverter.

  'a': (('c', ('q',)), ('q', 'b')) # Universal element.

  }


def view_register(r=R):
  names, values = zip(*sorted(r.iteritems()))
  print ''.join(names)
  print ''.join(str(int(not v)) for v in values)


program = dict((name, ()) for name in ascii_lowercase)


def cycle(register, program):
  next_values = register.copy()
  for bit in register:
    e = microcode[program[bit]]
    next_value = reify(register, e)
    next_values[bit] = reduce_(next_value)
  register.update(next_values)

#program['c'] = 'a'
while not raw_input('.'):
  view_register()
  cycle(R, program)
