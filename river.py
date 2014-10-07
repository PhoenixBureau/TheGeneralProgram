from egg import (Reduce, reify, s, void, mark,
                 view_register, cycle)

def nxor(a, b):
  return (a, (b,)), ((a,), b)

def xor(a, b):
  return (nxor(a, b),)


m, w, g, c= 'mwgc'

S = {
  (xor(m, w), nxor(g, c)): {m: (m,), w: (w,)},
  (xor(m, g),):            {m: (m,), g: (g,)},
  (xor(m, c), nxor(g, w)): {m: (m,), c: (c,)},
  (nxor(g, w), nxor(g, c)): {m: (m,)},
  }

R = {
  m: ((),),
  w: ((),),
  g: ((),),
  c: ((),),
  }

Target = {
  m: (),
  w: (),
  g: (),
  c: (),
  }

def ugh(d):
  return tuple(d[k] for k in sorted(d))

states = {}
stack = []
print ''.join(sorted('mwgc'))
prev = None
while R != Target:
  print view_register(R)
  u = ugh(R)
  if u in states:
    C = states[u]
  else:
    C = [S[e] for e in S
         if not(S[e] is prev)
         and mark(reify(R, e))
         ]
    states[u] = C
  while not C:
    if not stack:
      raise Exception("NOOOO")
    R, C = stack.pop()
    print 'backtracking to', view_register(R), C
  P = prev = C.pop(0)
  if C:
    stack.append((R.copy(), C))
    print 'remembering', view_register(R), C
  cycle(R, P)

print view_register(R)


