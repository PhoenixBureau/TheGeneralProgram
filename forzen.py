from itertools import combinations


class f(frozenset):

  def __repr__(self):
    r = (repr(inner) for inner in sorted(self))
    return '(' + ', '.join(r) + ')'

F = {}


def _f(form):
  return F.setdefault(form, form)

def comb(A):
  for n in xrange(1, len(A) + 1):
    for c in combinations(A, n):
      yield f(c)


a = _f(f())
b = _f(f([a]))


for n in comb(list(F)):
  print n
  _f(n)
for n in sorted(F):
  print n

print '*' * 23

for n in comb(list(F)):
  print n
  _f(n)
for n in sorted(F):
  print n

