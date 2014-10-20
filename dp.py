from egg import s


Mark = ()
Void = '_'


def dp(E, partial=None):
  if partial is None:
    partial = {}

  if not E:
    return partial

  print '[' + ', '.join(map(s, E)) + ']'
  if Mark in E:
    print
    return

  v = next_symbol_of(E)
  print 'trying', v, '= Mark'

  partial[v] = Mark
  Ev = list(vup(E, v))
  res = dp(Ev, partial)
  if res is not None:
    return res

  print 'trying', v, '= Void'
  partial[v] = Void
  Ev = list(puv(E, v))
  res = dp(Ev, partial)
  if res is not None:
    return res


def vup(E, v):
  n = v,
  for clause in E:
    if v in clause:
      continue
    yield tuple(i for i in clause if i != n)


def puv(E, v):
  n = v,
  for clause in E:
    if n in clause:
      continue
    yield tuple(i for i in clause if i != v)


def next_symbol_of(E):
  for clause in E:
    for term in clause:
      if isinstance(term, basestring):
        return term
      if term:
        return term[0]
  raise Exception("no more symbols")


a, b, c, d, e, f, g = 'abcdefg'

E = [
  # (a, (b,), c, b),
  ((a,), c, (d,)),
  (a, b, d),
  (b, (c,)),
  (a, (b,), (d,)),
  ]

H = [
  (a, (f,), (g,)),
  (f, (b,)),
  (f, (c,)),
  (g, (b,)),
  (g, (d,)),
  ((a,), (f,)),
  (b, c),
  (d, b),
  ]

G = [
  ((a,), b),
  ((b,), c),
  ((c,), d),
  ((c,), (d,)),
  ]

print
print dp(H)
