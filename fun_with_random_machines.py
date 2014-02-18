#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

  Gödel Machine

  [First attempt]


'''
from egg import *
from random import shuffle, random, choice


# Let there be a register of bits.
R = dict((name, ((),)) for name in ascii_lowercase)

def FBA(a, b, Cin):
  '''Full Bit Adder.'''
  k = xor(a, b)
  return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


Sum0, Cout = FBA('a', 'z', ((),))
Sum1, Cout = FBA('b', 'y', Cout)
Sum2, Cout = FBA('c', 'x', Cout)


# Let there be a set of expressions denoting transformations to apply
# to bits in the register to develop new bit-values for them.

##k = list(ascii_lowercase)
##shuffle(k)
##program = {}


##for k, v in zip(ascii_lowercase, k):
##  r = random()
##  if r < 0.14:
##    v = choice(ascii_lowercase), choice(ascii_lowercase)
##  program[k] = v
##  print k, ':', v
##print


program = {

##  'a': ('b',),
##  'b': 'a',

##  'd': ('f',),
##  'e': 'd',
##  'f': 'e',

##  'h': (('b', 'd',),),
##  'i': (('b', 'e',),),
##  'j': (('b', 'f',),),

##  'g': ('a', 's',),
##  'h': ('a', 'g',),
##  'i': ('a', 'h',),
##  'j': ('a', 'i',),
##
##  'l': ('b', 's',),
##  'm': ('b', 'g',),
##  'n': ('b', 'h',),
##  'o': ('b', 'i',),
##
##  'w': ('o', 's',),
##  'x': ('n', 'g',),
##  'y': ('m', 'h',),
##  'z': ('l', 'i',),

  'a': Sum0,
  'b': Sum1,
  'c': Sum2,

##  'y': (),

##  'l': Sum0,
##  'm': Sum1,
##  'n': Sum2,
  'o': Cout

##  'q': (('a', ('q',)), ('q', 'e')), # Universal element.
##

##  's': ('a', 'b'),
##  't': ('a', ('b',)),
##  'u': (('a',), 'b'),
##  'v': (('a',), ('b',)),
  }


def view_register(r=R):
  names, values = zip(*sorted(r.iteritems()))
##  print ''.join(names)
  return ''.join(str(int(not v)) for v in values
                 ).replace('0', '-').replace('1', 'o')


def cycle(register, program):
  next_values = register.copy()
  for bit in register:
    e = program.get(bit, bit)
    next_value = reify(register, e)
    next_values[bit] = reduce_(next_value)
  register.update(next_values)


##for i in range(20):
##  print view_register(R), i
##  cycle(R, program)


for x, y, z in product(B, B, B):
  print ascii_lowercase, y, x, z
  R = dict((name, ((),)) for name in ascii_lowercase)
  R['x'] = x
  R['y'] = y
  R['z'] = z

  r = {}
  i = 0
  v = view_register(R)
  while v not in r:
    r[v] = i
    cycle(R, program)
    v = view_register(R)
    print v, i
    i += 1



##  for i in range(20):
##    print view_register(R), i
##    cycle(R, program)
