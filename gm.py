#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from egg import *


# Let there be a register of bits.
R = dict((name, ((),)) for name in ascii_lowercase)

def FBA(a, b, Cin):
  '''Full Bit Adder.'''
  k = xor(a, b)
  return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


Sum, Cout = FBA('a', 'b', 'c')


# Let there be a set of expressions denoting transformations to apply
# to bits in the register to develop new bit-values for them.
program = {

#  'a': (Cout,),
  'a': Sum,
  'e': Cout,

  'q': (('a', ('q',)), ('q', 'e')), # Universal element.
  'p': (('d', ('p',)), ('p', 'e')),
  'j': (('d', ('j',)), ('j', 'e')),

  's': ('q', 'j'),
  't': ('q', ('j',)),
  'u': (('q',), 'j'),
  'v': (('q',), ('j',)),
  }


def view_register(r=R):
  names, values = zip(*sorted(r.iteritems()))
##  print ''.join(names)
  return ''.join(str(int(not v)) for v in values
                 ).replace('0', '-').replace('1', '○')


def cycle(register, program):
  next_values = register.copy()
  for bit in register:
    e = program.get(bit, bit)
    next_value = reify(register, e)
    next_values[bit] = reduce_(next_value)
  register.update(next_values)



for c, b, a in product(B, B, B):
#  print a, b, c, '=' * 30
  print ascii_lowercase, a, b, c
  R = dict((name, ((),)) for name in ascii_lowercase)
  R['a'] = a
  R['b'] = b
  R['c'] = c
  for i in range(18):
    print view_register(R), i
    cycle(R, program)

