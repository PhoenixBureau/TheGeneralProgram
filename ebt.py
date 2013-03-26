'''

  Every Bit Tells

Based on "Functional Pearl: Every Bit Counts"
by Dimitrios Vytiniotis & Andrew J. Kennedy
https://dl.acm.org/citation.cfm?id=1863548
'''

a = lambda n: n == 0
b = lambda n: n == 1
c = lambda n: n == 2


G = (a, (0, 1))


def decode(game, value):
  predicate, choices = game
  it = choices[not predicate(value)]
  if isinstance(it, tuple):
    return decode(it, value)
  return it
