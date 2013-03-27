
def encode(game, value):
  '''
  Return the path that encodes the value according to the game.
  '''
  next_predicate = game
  path = []
  while True:
    bit, next_predicate = next_predicate(value)
    path.append(int(bit))
    if not next_predicate:
      break
  return path


def decode(game, path):
  '''
  Return the value of the path for the game.
  '''
  for bit in path:
    if callable(game):
      game = game(bit)
    else:
      break
  return game


def map_it(game):
  '''
  Return the tree form of a game. The game should be total or you've
  entered an infinite loop.
  '''
  if not callable(game):
    return game

  try:
    left = map_it(game(1))
  except:
    return map_it(game(0))

  try:
    return left, map_it(game(0))
  except:
    return left


def decode_tree(game_tree, path):
  '''
  Return the value of the path for the game using the tree form of the game.
  '''
  for bit in path:
    try:
      game_tree = game_tree[not bit]
    except:
      pass
  return game_tree
