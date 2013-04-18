#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from pprint import pprint as p_
from egg import *


def FBA(a, b, Cin):
  '''
  Full Bit Adder.
  '''
  k = xor(a, b)
  return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


# Create expressions denoting a 3-bit adder circuit.
Sum0, Cout = FBA('a', 'z', ((),))
Sum1, Cout = FBA('b', 'y', Cout)
Sum2, Cout = FBA('c', 'x', Cout)
Sum3, Cout = FBA('d', 'w', Cout)

# Let there be a set of expressions denoting
# transformations to apply from bits in the
# register to develop new bit-values for them.
P = {

  # We will plug the output of the adder circuit
  # into one of its inputs to make a counter.
  'a': Reduce(Sum0),
  'b': Reduce(Sum1),
  'c': Reduce(Sum2),
  'd': Reduce(Sum3),

  'f': Reduce(Cout),

  }


# Let there be a register of bits.
R = dict.fromkeys(ascii_lowercase, ((),))


# Examine the behaviour of the system with various inputs.
for R['w'], R['x'], R['y'], R['z'] in product(B, B, B, B):

  # Simple header line.
  print ascii_lowercase, '%(w)s %(x)s %(y)s %(z)s' % R,

  # Run until the system returns to a previously seen state.
  detect_cycle(R, P)

  # Reset the register
  R = dict.fromkeys(ascii_lowercase, ((),))
