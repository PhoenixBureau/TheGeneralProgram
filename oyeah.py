#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from void import pretty, truth_table, value, reify


a, b = 'ab'
wxyz = (a, b), (a, (b,)), ((a,), b), ((a,), (b,))

for form in wxyz:
  print pretty(form) ; print
  truth_table(form) ; print ; print


w, x, y, z = 'wxyz'
a, b = ((y, z),), ((x, z),) # w is ignored.

_ = (), # Void
o = ()  # Mark

M = {}

A = lambda: value(reify(a, M))
B = lambda: value(reify(b, M))

print 'a =', pretty(a)
print 'b =', pretty(b)
print
print 'w x y z = a b'

for M[w], M[x], M[y], M[z] in (
  (_, _, _, _),
  (o, _, _, _),
  (_, o, _, _),
  (_, _, o, _),
  (_, _, _, o),
  ):
  display = {key: value(val) for key, val in M.items()}
  print '%(w)s %(x)s %(y)s %(z)s' % display, '=', A(), B()
