

B = ((),), ()


mark = lambda form: not form or not any(mark(inner) for inner in form)


reduce_ = lambda form: B[mark(form)]


nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(and_(bits))
xor = lambda *bits: nor(and_(*bits), nor(*bits))


def walk(meaning, name):
  while name in meaning and meaning[name] != name:
    name = meaning[name]
  if isinstance(name, tuple):
    return tuple(walk(meaning, inner) for inner in name)
  return name


def reify(meaning, form):
  if isinstance(form, basestring):
    return walk(meaning, form)
  if isinstance(form, tuple):
    return tuple(reify(meaning, inner) for inner in form)
  return form



########################################################################


intify = lambda n: int(bool(n))


from itertools import product


def FBA(a, b, Cin):
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, Cin)
  return nor(j, nor(y, Cin)), or_(j, h)


fba = FBA('a0', 'b0', 'Cin')


for a, b, c in product(B, B, B):
  meaning = {'a0': a, 'b0': b, 'Cin': c}
  su, co = reify(meaning, fba)
  print '%i + %i + %i = %i %i' % tuple(map(intify, (a, b, c, reduce_(su), reduce_(co))))



