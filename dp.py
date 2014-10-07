Mark = ()
Void = '_'


def dp(E, partial=None, symbols=None):

  if partial is None:
    assert symbols is None, repr(symbols)
    partial = {}
#    symbols = symbols_of(E)

  if not E:
    return partial

  if Mark in E:
    return

  v = next_symbol_of(E)
  print 'trying', v, '= Mark'

  partial[v] = Mark
  Ev = list(vup(E, v))
  print Ev
  res = dp(Ev, partial, symbols)
  if res is not None:
    return res

  print 'trying', v, '= Void'
  partial[v] = Void
  Ev = list(puv(E, v))
  print Ev
  res = dp(Ev, partial, symbols)
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


def symbols_of(E, seen=None):
  if seen is None:
    seen = set()
  for i in E:
    if isinstance(i, basestring):
      if i not in seen:
        seen.add(i)
        yield i
    else:
      for j in symbols_of(i, seen):
        yield j


def next_symbol_of(E):
  for clause in E:
    for term in clause:
      if isinstance(term, basestring):
        return term
      elif term:
        return term[0]
  raise Exception("no more symbols")


a, b, c, d, e = 'abcde'

E = [
  # (a, (b,), c, b),
  ((a,), c, (d,)),
  (a, b, d),
  (b, (c,)),
  (a, (b,), (d,)),
  ]

print
print dp(E)
