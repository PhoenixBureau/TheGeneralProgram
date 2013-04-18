#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from random import choice
from egg import *


def FBA(a, b, Cin):
  '''
  Full Bit Adder.
  '''
  k = xor(a, b)
  return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


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
    'a': Reduce(Sum0),
    'b': Reduce(Sum1),
    'c': Reduce(Sum2),

    'o': Reduce(Cout),

    }

  for ch in 'efghij':
    P[ch] = choice((nor, and_))(choice('abco'), choice('efghij'))
    print ch, ':', P[ch]

  # Examine the behaviour of the system with various inputs.
  for x, y, z in product(B, B, B):

    print ascii_lowercase, x, y, z, # Simple header li.

    # Let there be a register of bits.
    R = dict((name, ((),)) for name in ascii_lowercase)

    # Initialize the "free" input of the adder.
    R['x'] = x
    R['y'] = y
    R['z'] = z

    # Run until the system returns to a previously seen state.
    detect_cycle(R, P)

    #run_n_cycles(R, P, 20)
