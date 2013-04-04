# -*- coding: utf-8 -*-
from iota import O, S, K, I


B = (O, I)

D = {}
D[S] = 'S'
D[O] = 'i'
D[I] = 'I'
D[K] = 'K'

# S = λx.λy.λz.xz(yz)
# K = λx.λy.x
# i = λc.cSK

for x in B:
  for y in B:
    for z in B:
      f = S(x)(y)(z)
      print 'S', D.get(x, f), D.get(y, f), D.get(z, f), '=', D.get(f, 'I' if f(O) == O else '?')
