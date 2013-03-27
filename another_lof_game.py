#!/usr/bin/env python

def encode(game, value):
  '''
  Return the path that encodes the value according to the game.
  '''
  return map(int, game(value))

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
  q, p = {}, {}
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

    path = ''.join(map(str, encode(a_mark, form)))
    q[path] = form
    p[form] = path

    print '%-28s -> %s' % (form, path)
##    print '_' * 70

