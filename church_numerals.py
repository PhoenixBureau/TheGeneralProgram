# -*- coding: utf-8 -*-
'''
Freakin' Church numerals, man.

https://en.wikipedia.org/wiki/Church_encoding
'''

plus = lambda m: lambda n : lambda f: lambda x: m(f)(n(f)(x))
succ = lambda n: lambda f: lambda x: f(n(f)(x))
mult = lambda m: lambda n: lambda f: m(n(f))
exp = lambda m: lambda n: n(m)

c0 = lambda f: lambda x: x
c1 = lambda f: lambda x: f(x)
c2 = lambda f: lambda x: f(f(x))
c3 = lambda f: lambda x: f(f(f(x)))
c4 = plus(c1)(c3)
c5 = plus(c2)(c3)
c6 = plus(c1)(c5)
c7 = succ(c6)
c8 = succ(c7)
c9 = c3(succ)(c6)
c10 = mult(c2)(c5)
c11 = succ(c10)
c12 = mult(c3)(c4)
c64 = c3(c4)
c256 = exp(c2)(c8)


r = lambda n: 2 * n
p = lambda n: n + 1

print c3(r)(1)
print c4(r)(1)

print c5(p)(0)
print c6(p)(0)

print c7(r)(1)
print c7(p)(0)


##  β-reduction
##
##  Beta-reduction captures the idea of function application.
##  Beta-reduction is defined in terms of substitution:
##    the beta-reduction of  ((λV.E) E′)  is E[V := E′].
##
##  For example, assuming some encoding of 2, 7, ×,
##  we have the following β-reductions: ((λn.n×2) 7) → 7×2.

true = lambda a: lambda b: a
false = lambda a: lambda b: b

predicate = lambda n: true if n else false

print 't', predicate(True)(c2)(c3)(p)(0)
print 'f', predicate(False)(c2)(c3)(p)(0)
