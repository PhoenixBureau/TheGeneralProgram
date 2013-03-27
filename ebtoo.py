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


def encode(game, value):
  next_predicate = game
  path = []
  while True:
    bit, next_predicate = next_predicate(value)
    path.append(int(bit))
    if not next_predicate:
      break
  return path


def decode(game, path):
  for bit in path:
    game = game(bit)
  return game


def mapit(game):
  if not callable(game):
    return game

  try:
    left = mapit(game(1))
  except:
    return mapit(game(0))

  try:
    return left, mapit(game(0))
  except:
    return left


def decode_tree(game_tree, path):
  for bit in path:
    try:
      game_tree = game_tree[not bit]
    except TypeError:
      pass
  return game_tree


if __name__ == '__main__':
  e, d = make_a_game(3, 7)

  for n in range(3, 8):
    path = encode(e, n)
    print n, '->', path, '->', decode(d, path)

  print
  print mapit(d)

  print
  gt = mapit(d)
  for n in range(3, 8):
    path = encode(e, n)
    print n, '->', path, '->', decode_tree(gt, path)










