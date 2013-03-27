#!/usr/bin/env python

def encode(game, value):
  '''
  Return the path that encodes the value according to the game.
  '''
  next_predicate = game
  path = []
  while True:
    bits, next_predicate = next_predicate(value)
    path += map(int, bits)
    if not next_predicate:
      break
  return path

def a_mark(value):
  if value == ():
    return [0], None
  bits, f = A(value)
  return [1] + bits, f

def A(value):
  bits = encode(a_mark, value[0])
  if len(value) == 1:
    return [0] + bits, None
  bits += encode(a_mark, value[1:])
  return [1] + bits, None

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
