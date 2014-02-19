from void import void, reify, pretty


_ = (),
o = ()


def reduce_(form):
  return _ if void(form) else o


class Machine(object):

  def __init__(self, alphabet, program):
    self.R = dict.fromkeys(alphabet, _)
    self.P = program

  def cycle(self):
    next_values = self.R.copy()
    for bit, expression in self.P.iteritems():
      next_values[bit] = reduce_(reify(expression, self.R))
    self.R.update(next_values)

  def __repr__(self):
    return '[%s]' % (view_register(self.R),)

  def find_cycle(self, noisy=False):
    seen, n = {}, 0
    while True:
      s = str(self)
      if s in seen:
        return n, seen[s], sorted(seen, key=seen.get)
      if noisy:
        print ('%3i' % n), s
      seen[s] = n
      n += 1
      self.cycle()


def view_register(r):
  values = (r[bit] for bit in sorted(r))
  return ''.join(('-', 'o')[not v] for v in values)


def view_program(p):
  return '\n'.join(
    '%s: %s' % (bit, pretty(p[bit]))
     for bit in sorted(p)
    )

