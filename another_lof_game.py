#!/usr/bin/env python

def encode(game, value):
  '''
  Return the path that encodes the value according to the game.
  '''
  return game(value)

def a_mark(value):
  if value == ():
    return '0'
  bits = A(value)
  return '1' + bits

def A(value):
  bits = encode(a_mark, value[0])
  if len(value) == 1:
    return '0' + bits
  bits += encode(a_mark, value[1:])
  return '1' + bits

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

    path = encode(a_mark, form)
    q[path] = form
    p[form] = path

    print '%-28s -> %s' % (form, path),
    if path.endswith('0100'):
      print '~>', path[:-4] + 'x'
    else:
      print

##    print '_' * 70

