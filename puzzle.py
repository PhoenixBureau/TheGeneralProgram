'''
See http://markability.net/five_liars.htm
and http://iconicmath.com/mypdfs/bl-fiveliars.090625.pdf
to make some sense of this...
'''
from egg import xor, nxor, nand, or_, fstan, s
from egg import Reduce, s

def nxor(a, b):
  return (a, (b,)), ((a,), b)

def xor(a, b):
  return (nxor(a, b),)

a, b, c, d, e, f, g, h, i, j = 'abcdefghij'


tale = {

#===------------------------------------------------------------
#  A says:
#    a = Either B or D tells a Truth and a Lie.
#    f = Either C or E tells 2 Lies.
#
# a = [ [b|(g)] | ( [d|(i)] ) ]

  a: xor(nxor(b, g), xor(d, i)),  # same as nxor(nxor(b, g), nxor(d, i)) etc...

# f = ( [ (c)(h) | (e)(j) ] )

  f: nxor(nand(c, h), nand(e, j)),

#===------------------------------------------------------------
#  B says:
#    b = Either A or C tells a Truth and a Lie.
#    g = Either D tells 2 Lies or E tells 2 Truths.
#
# b = [ [a|(f)] | ( [c|(h)] ) ]

  b:  xor(nxor(a, f), xor(c, h)),

# g = ( [ (d)(i) | ej ] )

  g: nxor(nand(d, i), or_(e, j)),

#===------------------------------------------------------------
#  C says:
#    c = Either A or D tells 2 Truths.
#    h = Either B tells a Truth and a Lie or E tells 2 Lies.
#
# c = ( [af|di] )

  c: nxor(or_(a, f), or_(d, i)),

# h = ( [ [b|(g)] | (e)(j) ] )

  h: nxor(nxor(b, g), nand(e, j)),

#===------------------------------------------------------------
#  D says:
#    d = Either A or E tells 2 Lies.
#    i = Either B tells 2 Lies or C tells 2 Truths.

# d = ( [ (a)(f) | (e)(j) ] )

  d: nxor(nand(a, f), nand(e, j)),

# i = ( [ (b)(g) | ch ] )

  i: nxor(nand(b, g), or_(c, h)),

#===------------------------------------------------------------
#  E says:
#    e = Either A or B tells 2 Truths.
#    j = Either C or D tells a Truth and a Lie.

# e = ([af|bg])

  e : nxor(or_(a, f), or_(b, g)),

# j = ( [ [c|(h)] | [d|(i)] ] )

  j: xor(nxor(c, h), xor(d, i)),

#===------------------------------------------------------------
  }


# Conjunction of equivalence of each statements' symbol and "meaning":
E = or_(*(
  xor(name, expr)
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

if __name__ == '__main__':
  print 'Full expression:'
  print s(E)
  print
  print
  print
  print 'Standard form:'
  print s(Z)
  print
