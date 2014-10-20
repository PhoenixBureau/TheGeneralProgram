Void, Mark = ((),), ()


def pervade(form, remove=None):
  if remove is None:
    remove = set()

  names = set(
    n for n in form
    if isinstance(n, basestring)
    )
  names -= remove
  remove = remove | names
  subs = set()

  for t in form:
    if not isinstance(t, tuple):
      continue
    tt = pervade(t, remove)
    if not tt:
      return Void
    if tt == Void:
      continue
    subs.add(tt)

  return tuple(sorted(names)) + tuple(sorted(subs))


if __name__ == '__main__':
  from puzzle import E, Reduce, s


  e = Reduce(E)
  ee = pervade(e)

  j = 'a', ee
  jj = pervade(j)
  jjj = Reduce(jj)

  print len(s(E)), len(s(e)), len(s(ee))
  print len(s(j)), len(s(jj)), len(s(jjj))


  for t in E[0]:
    print s(t)
