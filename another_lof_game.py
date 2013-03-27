#!/usr/bin/env python

def encode(game, value):
  '''
  Return the path that encodes the value according to the game.
  '''
  path = []
  bits = game(value)
  path += map(int, bits)
  return path

def a_mark(value):
  if value == ():
    return [0]
  bits = A(value)
  return [1] + bits

def A(value):
  bits = encode(a_mark, value[0])
  if len(value) == 1:
    return [0] + bits
  bits += encode(a_mark, value[1:])
  return [1] + bits

if __name__ == '__main__':
  for form in (
    (),
    ((),),
    ((), (),),
    ((), (), (),),
    ((), (), (), (),),
    (((),),),
    (((),), ()),
    ((), ((),),),
    (((),), ((),)),
    (((),), ((),), ((),)),
    (((),), ((),), ((),), ((),)),
    ((((),),),),
    ):
    print form, '->', encode(a_mark, form)
    print '_' * 70
