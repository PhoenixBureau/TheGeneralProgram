#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from void import pretty, truth_table, value, reify


nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(map(nor, bits))
nand = lambda *bits: nor(and_(*bits))
xor = lambda x, y: nor(and_(x, y), nor(x, y))
XOR = lambda a, b: (((a, (b,)), ((a,), b)),)

a, b = 'ab'
for op in (or_, nor, and_, nand, xor, XOR):
  print pretty(op(a, b)) ; print


def FBA(a, b, carry_in):
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, carry_in)
  return nor(j, nor(y, carry_in)), or_(j, h)


sum0, carry_out = FBA('a0', 'b0', 'Cin')
sum1, carry_out = FBA('a1', 'b1', carry_out)
sum2, carry_out = FBA('a2', 'b2', carry_out)


print 'Full-Bit Adder'
print pretty(sum0) ; print
print pretty(sum1) ; print
print pretty(sum2) ; print
print pretty(carry_out) ; print
print

##w, x, y, z = 'wxyz'
##a, b = ((y, z),), ((x, z),) # w is ignored.
##
##_ = (), # Void
##o = ()  # Mark
##
##M = {}
##
##A = lambda: value(reify(a, M))
##B = lambda: value(reify(b, M))
##
##print 'a =', pretty(a)
##print 'b =', pretty(b)
##print
##print 'w x y z = a b'
##
##for M[w], M[x], M[y], M[z] in (
##  (_, _, _, _),
##  (o, _, _, _),
##  (_, o, _, _),
##  (_, _, o, _),
##  (_, _, _, o),
##  ):
##  display = {key: value(val) for key, val in M.items()}
##  print '%(w)s %(x)s %(y)s %(z)s' % display, '=', A(), B()
