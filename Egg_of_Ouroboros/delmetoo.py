from egg import dpll, frozenset_converter as convert


Form = frozenset


def tg(edges, colors='_red _blue _green'.split()):
  V = set()

  # For each edge...
  for v1, v2 in edges:
    V.add(v1) # (Remember the verts for later.)
    V.add(v2)
    # ...and color...
    for color in colors:
      # ... the two vertices can't both be that color.
      yield (v1 + color, v2 + color)

  # Each vertex must have a color.
  for v in V:
    yield tuple((v + color,) for color in colors)


if __name__ == '__main__':

  a, b, c, d = 'abcd'

  triangle = ((a, b), (b, c), (c, a))

  uncolorable = (
    (a, b),
    (b, c),
    (c, d),
    (a, d),
    (b, d),
    (a, c),
    )

  H = convert(tg(triangle))
  print H
  print
  print [k for k, v in dpll(H).items() if v]


for pigeon in range(1, 4):
  for hole in range(1, 3):
    exec 'a%i%i = "%i%i"' % (pigeon, hole, pigeon, hole)


P = PIGEONHOLE = convert([
  (a11, a12), (a21, a22), (a31, a32),
  ((a11,), (a21,)), ((a11,), (a31,)), ((a12,), (a22,)),
  ((a12,), (a32,)), ((a21,), (a31,)), ((a22,), (a32,)),
  ])

def literals(E):
  return set(term for term in E if isinstance(term, basestring))



def insertion(E):
  for into in E:
    put = E.difference({into})
    return into, put


def find_literals(into, stack=None):
  if stack is None:
    stack = []

  lits = literals(into)
  if lits:
    return lits, into, stack

  stack.append(into)
  for i in into:
    lits, i, stack = find_literals(i, stack)
    if lits:
      return lits, i, stack



##i, p = insertion(P)
##lits, lilput, trail = find_literals(i)
##
##simpl = p.K(lits, {})

#k = i | P.difference({i})





def remy(T):
  k = len(s(T))
  while True:
    Y = Reduce(pervade(T))
    j = len(s(Y))
    if j >= k:
      return T
    T, k = Y, j


def sorter(A, B, J, K, H, L, reset):
  jq = ((A,), B)
  kq = ((B,), A)
  return {
    J: ((J, jq), reset),
    K: ((K, kq), reset),
    L: (((J,), A), (J, B)),
    H: (((K,), B), (K, A)),
    }


##U = ('A', 'B', 'J', 'K', 'H', 'L', 'reset')
##S = sorter(*U)
##
##for k, v in S.items():
##  print k, s(v)
##print


def _bits_in(i):
  return (
    bool(i & 2**n)
    for n in (range(len(bin(i)) - 2))
    )

def z(a, b):
  for ga, gb in zip(_bits_in(a), _bits_in(b)):
    r = set()
    if ga: r.add('A')
    if gb: r.add('B')
    yield r


##Z = z(20, 19)
###Z = z(19, 20)
###Z = z(23, 18)
##R = next(Z)
##_o = ''.join(name[0] for name in U)
##print '%s    %s' % (_o, _o[2:])
##for _ in range(30):
##  D = cycle(R, S)
##  print _view(R, U), '->', _view(D, U[2:])
####  print R
####  print D
##  D = D - {"A", "B"}
####  print D
##  R = next(Z) #& D
####  print R | D
####  print
##  R = R | D
##
##print _view(R, U)




def pargen(left, right=0, ans=''):
  if not (left or right):
    yield ans
    return
  if left > 0:
    for i in pargen(left - 1, right + 1, ans + '('):
      yield i
  if right > 0:
    for i in pargen(left, right - 1, ans + ')'):
      yield i

##for n in range(1, 11):
##  print '=' * 10
##  print n
##  for b in pargen(n):
##    print '.' * 10
##    print b,
##    print b.replace(')', '),'),
##    print eval(b.replace(')', '),'))
    

#############################################################################################################

def walk(meaning, name, seen=None):
  if seen is None:
    seen = set()
  while name in meaning and meaning[name] != name:
    name = meaning[name]
    if name in seen:
      break
    seen.add(name)
  if isinstance(name, tuple):
    return tuple(walk(meaning, inner) for inner in name)
  return name


def reify(meaning, form):
  if isinstance(form, basestring):
    try:
      return walk(meaning, form)
    except RuntimeError:
      return form
  if isinstance(form, tuple):
    return tuple(reify(meaning, inner) for inner in form)
  return form


def assoc(meaning, key, value):
  d = meaning.copy()
  d[key] = value
  return d


def goal_clause(terms):
  return nor(and_(*terms))


##def unify(u, v, s, eq=eq):
##  """
##  Find substitution so that u == v while satisfying s
##
##  >>> unify((1, x), (1, 2), {})
##  {x: 2}
##
##  """
##  u = walk(s, u)
##  v = walk(s, v)
##  if eq(u, v):
##    return s
##  if isinstance(u, basestring):
##    return assoc(s, u, v)
##  if isinstance(v, basestring):
##    return assoc(s, v, u)
##  if isinstance(u, tuple) and isinstance(v, tuple):
##    if len(u) != len(v):
##      return False
##    for uu, vv in zip(u, v):  # avoiding recursion
##      s = unify(uu, vv, s, eq)
##      if s == False: # (instead of a Substitution object.)
##        break
##    return s
##  return False


def cycle(register, program):
  '''
  Run one cycle of the program on the register.
  '''
  next_values = register.copy()
  for bit in register:
    next_value = reify(register, program.get(bit, bit))
    next_values[bit] = reduce_(next_value)
  register.update(next_values)


def view_register(r):
  '''
  Return a string representation of a register for insight.
  '''
  values = (r[bit] for bit in sorted(r))
  return ''.join(('-', 'O')[not v] for v in values)


def run_n_cycles(r, p, n=10, view=True):
  for i in range(n):
    if view:
      print view_register(r), i
    cycle(r, p)


def detect_cycle(r, p, view=True):
  seen = {}
  i = 0
  v = view_register(r)

  while v not in seen:
    if view:
      print
    seen[v] = i

    cycle(r, p)

    v = view_register(r)
    if view:
      print v, i,

    i += 1

  if view:
    print seen[v] - 1




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


##from egg import Mark, Void
##
##
##if __name__ == '__main__':
##  from egg import solve, Reduce, s, INS, normalize, pervade
##  from dll import H, G, convert, Form
##  from delmetoo import P
##  from puzzle import E
##
##  E = normalize(Reduce((E[0])))
##  W = INS(E)

#  print INS(G)
##  a, b, c = 'abc'
##
##  E = convert((
##    a,
##    ((b,), (c,)),
##    (
##      ((a, b,), (a, c,)),
##    ), 
##    ))
##  i = INS(E)
##  print '-' * 40
##  print E, '->', i
##  print '-' * 40
##
##  E = convert((
##    (
##      a,
##      ((b,), (c,)),
##    ),
##    ((a, b,), (a, c,)), 
##    ))
##  i = INS(E)
##  print '-' * 40
##  print E, '->', i
##  print '-' * 40


##if __name__ == '__main__':

##  e = Reduce(E)
##  ee = pervade(e, set())
##
##  j = 'a', ee
##  jj = pervade(j, set())
##  jjj = convert(Reduce(jj))
##
##  print len(s(E)), len(s(e)), len(s(ee))
##  print len(s(j)), len(s(jj)), len(s(jjj))
##
##
##  print jjj






##def assign_mark(form, v):
##  if form == v: return Mark
##  if isinstance(form, basestring): return form
##  return type(form)(assign_mark(inner, v) for inner in form)
##
##
##def assign_void(form, v):
##  if form == v: return Void
##  if isinstance(form, basestring): return form
##  return type(form)(assign_void(inner, v) for inner in form)
##
##
##def reduce_(form):
##  if isinstance(form, basestring): return form
##  a = []
##  for inner in form:
##    inner = reduce_(inner)
##    if not inner: # Mark
##      return Void
##    if inner != Void:
##      a.append(inner)
##  return type(form)(a)


##print H
##j = occlude_pervade(H, {'a', 'f'}, {'c'})
##print j
##
##print
##
##print H
##j = occlude_pervade(H, {'b'}, ())
##print j


'''





"Plain" Insertion fails 


((c)(b)) <- [((c)(b))] -> [((c)(b))]
(c) <- [((c)(b))] -> []
(b) <- [((c)(b))] -> []


((c)(b) ((c)(b)) )    -> [((c)(b))]
 (c ((c)(b)) )        -> [(( )(b))]
 (c (( )(b)) )        -> [(( )   )]
 (c (( )   ) )        -> [_]
 (c          )        -> []


((c)(b) ((c)(b)) )    -> [((c)(b))]
((c)(b) (   (b)) )    -> [(   (b))]
((c)(b) (      ) )    -> [(      )]
(       (      ) )    -> [O]
                      -> _






a ((c)(b)) ((ac)(ab))

into a
put [((c)(b)), ((ac)(ab))]
returned a


into ((ac)(ab))
put ['a', ((c)(b))]
((ac)(ab)) <- ['a', ((c)(b))] -> ['a', ((c)(b))]
  (a c) <- ['a', ((c)(b))] -> []
  (a b) <- ['a', ((c)(b))] -> []
returned ((ac)(ab))


into ((c)(b))
put ['a', ((ac)(ab))]
((c)(b)) <- ['a', ((ac)(ab))] -> ['a', ((c)(b))]
  (c) <- ['a', ((c)(b))] -> ['a']
  (b) <- ['a', ((c)(b))] -> ['a']
returned ((c)(b))






Reduction of Pigeonhole (the * marks the semi-fail step)

  ((21)(11)) <- ((2122)((21)(31))((22)(12))((31)(11))((22)(32))((12)(32))(3231)(1112))
  ((21)(11)) <- ((2122)(    (31))((22)(12))((31)    )((22)(32))((12)(32))(3231)(1112)) subsume (11), (21)
  ((21)(11)) <- ((2122)      31  ((22)(12))  31      ((22)(32))((12)(32))(3231)(1112)) reduce
  ((21)(11)) <- ((2122)          ((22)(12))  31      ((22)(32))((12)(32))(32  )(1112)) pervade 31
  ((21)(11)) <- ((2122)          ((22)(12))  31      ((22)    )((12)    )(32  )(1112)) pervade (32)
  ((21)(11)) <- ((2122)          ((22)(12))  31        22        12      (32  )(1112)) reduce
  ((21)(11)) <- ((21  )          ((  )(  ))  31        22        12      (32  )(11  )) pervade 22, 12
 *((21)(11)) <- ((21  )                      31        22        12      (32  )(11  )) reduce
  ((21)(11)) <- (                            31        22        12      (32  )      ) (re-)pervade (11), (21)
  ((21)(11)) <- (31 22 12 (32))                                                        Failure!
  ((21)(11) 31 22 12 (32))                                                             Failure!

  Proceed with insertion to next depth rather than (re-)subsume (11) and (21):
 *((21)(11)) <- ((21  )                      31        22        12      (32  )(11  ))
  ((21)(11)) <- ((21) 31 22 12 (32)(11))
  ((21                        )(11                        )) <- ((21) 31 22 12 (32)(11))
  ((21 (21) 31 22 12 (32)(11) )(11 (21) 31 22 12 (32)(11) )) <- ((21) 31 22 12 (32)(11)) ins
  ((21 (  ) 31 22 12 (32)(11) )(11 (21) 31 22 12 (32)(  ) )) <- ((21) 31 22 12 (32)(11)) pervade 21, 11
  ((   (  )                   )(                     (  ) )) <- ((21) 31 22 12 (32)(11)) occlusion
  (                                                        ) <- ((21) 31 22 12 (32)(11)) ()



'''


#################################################

from egg import s


Mark = ()
Void = Mark,


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
print dp(G)



############################################################

from pprint import pprint
from egg import void, s, all_meanings


##def pargen(left, right=0, ans=''):
##  if not (left or right):
##    yield ans
##    return
##  if left > 0:
##    for i in pargen(left - 1, right + 1, ans + '('):
##      yield i
##  if right > 0:
##    for i in pargen(left, right - 1, ans + '),'):
##      yield i


def N():
  n = 0
  while True:
    yield str(n)
    n += 1


def pargen(left, right=0, ans='', rank=0):
  if not rank:
    rank = left
  if not (left or right):
    yield ans
    return
  n = str(rank - left) + ','
  if left > 0:
    for i in pargen(left - 1, right + 1, ans + '(a' + n, rank):
      yield i
  if right > 0:
    for i in pargen(left, right - 1, ans + '),', rank):
      yield i

def megaeval(form, do):
  if isinstance(form, basestring):
    return eval(form, do)
  else:
    return type(form)(megaeval(i, do) for i in form)


##do['a0'] = 'bool(23)'
##megaeval(E, do)


def cmpy(k, y):
  Mku, Mkd = D[k]
  Myu, Myd = D[y]
  l, r = ((Mku | Myd) == S), ((Mkd | Myu) == S)
  if l and r: return 0
  if l: return 1
  return -1

harden = lambda m: frozenset(m.iteritems())


N = 4
#do = {'a'+str(i): () for i in range(N)}

do = {n:n for n in ('a'+str(i) for i in range(N))}

Z = list(pargen(4))
B = list(all_meanings(do))
b = map(harden, B)
S = set(b)


D = {}
for e in Z:
  d = D[e] = (set(), set())
  for m, h in zip(B, b):
    d[void(eval(e, {}, m))].add(h)


##for k in D:
##  print '=' * 10
##  for y in D:
##    if k == y:
##      continue
##    eq = ('>=', ' == ', '<=')[cmpy(k, y) + 1]
##    print k, eq, y

def _u(m):
  return ' '.join(sorted(k for k, v in m if not v))

for e in sorted(D, cmp=cmpy):
  u, d = D[e]
  u = sorted(map(_u, u))
  d = sorted(map(_u, d))
  print e
  print '=' * 10
  pprint(u)
  pprint(d)
  print '-' * 10





##E = eval(e, do)
##print e, s(E)


##if __name__ == '__main__':
##  from pprint import pprint
##  from collections import defaultdict
##  from dll import convert
##  from egg import void, depth
##
##  A = set()
##  c = 0
##  n = 2
##  N = 10000
##  while len(A) < N:
##    print n
##    for e in pargen(n):
##      A.add(convert(eval(e)))
##      c += 1
##      if len(A) >= N:
##        break
##    n += 1
##  pprint(sorted(A, key=depth))
##  print c



##  M, V, D = [], [], defaultdict(list)
##  for n in range(2, 20):
##    print '=' * 10
##    print n
##    for e in pargen(n):
##      t = eval(e)
##      c = convert(t)
##      (M, V)[not void(c)].append(c)
##      D[c].append(e.replace(',', ''))
##      print e, t, c

##  pprint(dict(D))
#      print '%s %s %s' % (e, R(e), ooo(e))


##for e in (
##  '((()())(())(()())(()())(()())()())',
##  '(((()())(())(()())(()())(()())()()))',
##  '()()()()()',
##  '(()()()()())',
##  '(()(()(()()())))',
##  ):
##  print e
##  print R(e)
##  print ooo(e)
##  print '=' * 8





a, b, c, d, e, f, g = 'abcdefg'


E = (
  # (a, (b,), c, b),
  ((a,), c, (d,)),
  (a, b, d),
  (b, (c,)),
  (a, (b,), (d,)),
  )

H = (
  (a, (f,), (g,)),
  (f, (b,)),
  (f, (c,)),
  (g, (b,)),
  (g, (d,)),
  ((a,), (f,)),
  (b, c),
  (d, b),
  )

G = (
  ((a,), b),
  ((b,), c),
  ((c,), d),
  ((c,), (d,)),
  )


if __name__ == '__main__':
  from egg import dpll, s, frozenset_converter
  E, H, G = map(frozenset_converter, (E, H, G))
  print
  print '=' * 40
  print s(E)
  print dpll(E)
  print
  print '=' * 40
  print s(H)
  print dpll(H)
  print
  print '=' * 40
  print s(G)
  print dpll(G)
  print
