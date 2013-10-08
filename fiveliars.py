'''
See http://markability.net/five_liars.htm
and http://iconicmath.com/mypdfs/bl-fiveliars.090625.pdf
to make some sense of this...
'''
from egg import eqiv, xor, nand, or_, fstan, s


a, b, c, d, e, f, g, h, i, j = 'abcdefghij'


tale = {

#===------------------------------------------------------------
#  A says:
#    a = Either B or D tells a Truth and a Lie.
#    f = Either C or E tells 2 Lies.
#
# a = [ [b|(g)] | ( [d|(i)] ) ]

  a: eqiv(xor(b, g), eqiv(d, i)),  # same as xor(xor(b, g), xor(d, i)) etc...

# f = ( [ (c)(h) | (e)(j) ] )

  f: xor(nand(c, h), nand(e, j)),

#===------------------------------------------------------------
#  B says:
#    b = Either A or C tells a Truth and a Lie.
#    g = Either D tells 2 Lies or E tells 2 Truths.
#
# b = [ [a|(f)] | ( [c|(h)] ) ]

  b:  eqiv(xor(a, f), eqiv(c, h)),

# g = ( [ (d)(i) | ej ] )

  g: xor(nand(d, i), or_(e, j)),

#===------------------------------------------------------------
#  C says:
#    c = Either A or D tells 2 Truths.
#    h = Either B tells a Truth and a Lie or E tells 2 Lies.
#
# c = ( [af|di] )

  c: xor(or_(a, f), or_(d, i)),

# h = ( [ [b|(g)] | (e)(j) ] )

  h: xor(xor(b, g), nand(e, j)),

#===------------------------------------------------------------
#  D says:
#    d = Either A or E tells 2 Lies.
#    i = Either B tells 2 Lies or C tells 2 Truths.

# d = ( [ (a)(f) | (e)(j) ] )

  d: xor(nand(a, f), nand(e, j)),

# i = ( [ (b)(g) | ch ] )

  i: xor(nand(b, g), or_(c, h)),

#===------------------------------------------------------------
#  E says:
#    e = Either A or B tells 2 Truths.
#    j = Either C or D tells a Truth and a Lie.

# e = ([af|bg])

  e : xor(or_(a, f), or_(b, g)),

# j = ( [ [c|(h)] | [d|(i)] ] )

  j: eqiv(xor(c, h), eqiv(d, i)),

#===------------------------------------------------------------
  }


# Conjunction of equivalence of each statements' symbol and "meaning":
E = or_(*(
  eqiv(name, expr)
  for name, expr in tale.iteritems()
  ))

# Find the normalized standard form.
Z = fstan(E)

# E is huge, but in this case Z is quite tractable:
#
# Z = ( (a(b)(c)(d)(e)(f)g h(i)j) ((a)b(c)(d)e f g(h)(i)(j)) )
#
# i.e.: (
#  ( a (b)(c)(d)(e)
#   (f) g  h (i) j )
#
#  ((a) b (c)(d) e
#    f  g (h)(i)(j))
#  )
#
# ...are the two answers.  Neat.

print 'Full expression:'
print s(E)
print
print
print
print 'Standard form:'
print s(Z)
print
