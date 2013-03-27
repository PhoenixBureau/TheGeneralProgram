

def make_a_game(from_=0, to=10):

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


e, d = make_a_game(3, 7)


for n in range(3, 8):
  path = encode(e, n)
  print n, '->', path, '->', decode(d, path)
