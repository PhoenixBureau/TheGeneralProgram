#!/usr/bin/env python


def make_a_game(from_=0, to=10):
  '''
  The "dumb" game.
  '''

  def encode(value):
    if value > to or value < from_:
      raise ValueError(value)
    if value == from_:
      return 1, None
    return 0, make_a_game(from_ + 1, to)[0]

  def decode(bit, n=from_):
    if n > to or n < from_:
      raise ValueError(n)
    if bit:
      return n
    return lambda bit_: decode(bit_, n + 1)

  return encode, decode



if __name__ == '__main__':
  from ebtoo import encode, decode, map_it, decode_tree
  e, d = make_a_game(3, 7)

  for n in range(3, 8):
    path = encode(e, n)
    print n, '->', path, '->', decode(d, path)

  print
  print map_it(d)

  print
  gt = map_it(d)
  for n in range(3, 8):
    path = encode(e, n)
    print n, '->', path, '->', decode_tree(gt, path)










