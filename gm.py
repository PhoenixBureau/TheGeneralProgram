#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from egg import *


def FBA(a, b, Cin):
  '''
  Full Bit Adder.
  '''
  k = xor(a, b)
  return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


def cycle(register, program):
  '''
  Run one cycle of the program on the register.
  '''
  next_values = register.copy()
  for bit in register:
    next_value = reify(register, program.get(bit, bit))
    next_values[bit] = reduce_(next_value)
  register.update(next_values)


def view_register(r):
  '''
  Return a string representation of a register for insight.
  '''
  values = (r[bit] for bit in sorted(r))
  return u''.join(u'-○'[not v] for v in values)


def run_n_cycles(r, p, n=10, view=True):
  for i in range(n):
    if view:
      print view_register(r), i
    cycle(r, p)


def detect_cycle(r, p, view=True):
  seen = {}
  i = 0
  v = view_register(r)
  while v not in seen:
    seen[v] = i
    cycle(r, p)
    v = view_register(r)
    if view:
      print v, i
    i += 1


if __name__ == '__main__':

  # Create expressions denoting a 3-bit adder circuit.
  Sum0, Cout = FBA('a', 'z', ((),))
  Sum1, Cout = FBA('b', 'y', Cout)
  Sum2, Cout = FBA('c', 'x', Cout)

  # Let there be a set of expressions denoting
  # transformations to apply from bits in the
  # register to develop new bit-values for them.
  P = {

    # We will plug the output of the adder circuit
    # into one of its inputs to make a counter.
    'a': Sum0,
    'b': Sum1,
    'c': Sum2,

    'o': Cout

    }

  # Examine the behaviour of the system with various inputs.
  for x, y, z in product(B, B, B):

    print ascii_lowercase, y, x, z # Simple header li.

    # Let there be a register of bits.
    R = dict((name, ((),)) for name in ascii_lowercase)

    # Initialize the "free" input of the adder.
    R['x'] = x
    R['y'] = y
    R['z'] = z

    # Run until the system returns to a previously seen state.
    detect_cycle(R, P)
