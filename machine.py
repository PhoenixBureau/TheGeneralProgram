from egg import Reduce, normalize
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
    self.R.update({
      bit: reduce_(reify(expression, self.R))
      for bit, expression in self.P.iteritems()
      })

  def __repr__(self):
    return '[%s]' % (view_register(self.R),)

  def find_cycle(self, noisy=False):
    seen, n = {}, 0
    while True:
      i = self.as_int()
      if i in seen:
        return n, seen[i], sorted(seen, key=seen.get)
      if noisy:
        print ('%3i' % n), self
      seen[i] = n
      n += 1
      self.cycle()

  def save(self, file_ish):
    import pickle
    pickle.dump(self, file_ish)

  def reset(self):
    for bit in self.R:
      self.R[bit] = _

  def as_int(self):
    g = (
      (n, self.R[bit])
      for n, bit in
      enumerate(sorted(self.R, reverse=True))
      )
    return sum(2**n for n, bit in g if not bit)


def view_register(r):
  values = (r[bit] for bit in sorted(r))
  return ''.join(('-', 'o')[not v] for v in values)


def view_program(p):
  return '\n'.join(
    '%s: %s' % (bit, pretty(p[bit]))
     for bit in sorted(p)
    )


nor = lambda *bits: bits
or_ = lambda *bits: (bits,)
and_ = lambda *bits: tuple((bit,) for bit in bits)
nand = lambda *bits: (and_(*bits),)
xor = lambda x, y: (((x, (y,)), ((x,), y)),)


ifthen = lambda q, a, b: ((a, (q,)), (q, b))
flipflop = lambda q, r, s: ((s, q), r)


def FBA(a, b, c):
  '''Full Bit Adder.'''
  k = xor(a, b)
  return xor(k, c), or_(and_(k, c), and_(a, b))


def make_adder(reg0, reg1):
  if len(reg0) != len(reg1):
    raise ValueError
  bits, carry = [], _
  for r0, r1 in zip(reg0, reg1):
    sum_bit, carry = FBA(r0, r1, carry)
    bits.append(normalize(Reduce(sum_bit)))
  return bits, normalize(Reduce(carry))


def make_switch(q, reg0, reg1):
  if len(reg0) != len(reg1):
    raise ValueError
  return tuple(ifthen(q, r0, r1) for r0, r1 in zip(reg0, reg1))
