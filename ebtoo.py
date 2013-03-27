

def make_a_game(from_=0, to=10):
  def game(value):
    if value > to:
      raise ValueError(value)
    if value == from_:
      return 1, None
    return 0, make_a_game(from_ + 1, to)
  return game


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


def g(bit, n=0):
  if bit:
    return n
  def g_(bit_):
    return g(bit_, n + 1)
  return g_
  


G = make_a_game()

for n in range(11):
  path = encode(G, n)
  print n, '->', path, '->', decode(g, path)
