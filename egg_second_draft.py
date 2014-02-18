# -*- coding: utf-8 -*-
# This is the Egg of Ouroborous a book about the Laws of Form in the form
# of a Python module.  I hope to create a simple and powerful way to
# construct computer software that can be easily taught to any bright
# person, and I hope to introduce those already familiar with computer
# programming to the wonders and joy of this discovery.

# The following imports will be explained where they are used.  You
# should consult the Python documentation if you have questions about the
# basic function of these.
from itertools import product, imap, izip
from operator import eq
from string import ascii_lowercase
from collections import defaultdict


# The Laws of Form begin from nothing with the making of a disticntion
# that separates the world into three parts: the boundary, one side, and
# the other side.  We will represent the making of a distinction by a
# closed figure (paired parentheses) which, in Python, are immutable
# collections of values called "tuples".

# There are two basic rules (the Bricken Basis) for the boundary forms
# that allow us to transform forms without altering their total value.
# These rules are:
#
#     ()() = ()
#
#     (()) =
#
# That second rule has nothing on the right hand side. The Laws of Form
# concern not a binary true/false logic but rather a unitary existance
# based logic wherein true statements exist but "false" statements
# evaporate into nothingness.

# Because it is not possible to represent nothing in a computer we must
# "map" the double form (()) onto the "Void" giving a managable Bineray
# Boolean domain B:

B = ((),), ()


# To discover the Boolean truth value of a form we construct a function
# that examines that form, recursively if neccessary.

# The imap() function is a "lazy" form of map that only evaluates as
# asked, since the any() built-in function is also "lazy"
# (short-circuiting evaluation of its arguments as soon as if finds a
# True value) this prevents the algorith from continuing the search
# unnecessarily.

mark = lambda form: not form or not any(imap(mark, form))


# We can use the domain B above to recover the form of the reduced form

reduce_ = lambda form: B[mark(form)]

# There is a wrinkle here due to the fact that Python uses tuples to
# group things. If we want to treat several forms next to each other on
# the "top" level we have to enclose them within two tuples before
# passing them to be processed.  Otherwise Python's automatic grouping
# will add a spurious tuple around them and invert their value.  So the
# following form:
#
#  form = (), (), ()
#
# Instead has to be:
#
#  form = (((), (), ()),)
#
# In order for the reduce_() function to work properly:
#
#  >>> form = (((), (), ()),)
#  >>> reduce_(form)
#  ()
#
#  >>> form = (), (), ()
#  >>> reduce_(form)
#  ((),)
#


# We can use the following functions to build up forms that represent
# electronic circuits and logical statements:

nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(and_(bits))
xor = lambda *bits: nor(and_(*bits), nor(*bits))

# For example, this is one way to construct an adder circuit:

def FBA(a, b, Cin):
  '''Full Bit Adder, factored.'''
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, Cin)
  return nor(j, nor(y, Cin)), or_(j, h)


# We can then build a four-bit adding circuit by ganging together

Sum0, Cout0 = FBA('a0', 'b0', 'Cin')
Sum1, Cout1 = FBA('a1', 'b1', Cout0)
Sum2, Cout2 = FBA('a2', 'b2', Cout1)
Sum3, Cout3 = FBA('a3', 'b3', Cout2)

adder = {
  'Sum0': Sum0,
  'Sum1': Sum1,
  'Sum2': Sum2,
  'Sum3': Sum3,
  'Carry': Cout3,
  }


# This is a rather unwieldy tuple of tuples so let's create a simple
# string formatter function to print them nicely.

s = lambda term: (str(term)
                  .replace(' ', '')
                  .replace("','", ' ')
                  .replace("'", '')
                  .replace(',', '')
                  .replace('(())', '◎')
                  .replace('()', '○')
                  )


##  >>> for output_signal in sorted(adder):
##          print output_signal, s(adder[output_signal])
##          print
##
##
##  Carry (((((((a3)(b3))(a3 b3)))((((((((a2)(b2))(a2 b2)))((((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((a1)(b1))))))((a2)(b2))))))((a3)(b3))))
##
##  Sum0 ((((((a0)(b0))(a0 b0)))(Cin))((((a0)(b0))(a0 b0))Cin))
##
##  Sum1 ((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((((a1)(b1))(a1 b1))(((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))
##
##  Sum2 ((((((a2)(b2))(a2 b2)))((((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((a1)(b1))))))((((a2)(b2))(a2 b2))(((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((a1)(b1))))))
##
##  Sum3 ((((((a3)(b3))(a3 b3)))((((((((a2)(b2))(a2 b2)))((((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((a1)(b1))))))((a2)(b2))))))((((a3)(b3))(a3 b3))(((((((a2)(b2))(a2 b2)))((((((((a1)(b1))(a1 b1)))((((((((a0)(b0))(a0 b0)))(Cin))((a0)(b0))))))((a1)(b1))))))((a2)(b2))))))

# So those are pretty hairy but we can simulate their operation by
# substituting real values for the string placeholders and reducing.

# First we need a function to collect the names in a form (or collection
# of forms such as our "adder".

def collect_names(form, names=None):
  if names is None:
    names = set()
  if isinstance(form, basestring):
    names.add(form)
  else:
    for inner in form:
      collect_names(inner, names)
  return names


# Then we can use that (and the itertools.product() function) to create inputs for a "truth table"
# in the form of dictionaries mapping the names in a form to each possible set of values (from B)
# for those names.

def all_meanings(form):
  names = sorted(collect_names(form))
  for values in product(*([B] * len(names))):
    yield dict(izip(names, values))

##  for M in all_meanings(adder.values()):
##    for input_signal in sorted (M):
##      print input_signal, int(mark(M[input_signal])), ',',
##    print
##
##  >>> 
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 0 , b2 0 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 0 , b2 0 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 0 , b2 1 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 0 , b2 1 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 1 , b2 0 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 1 , b2 0 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 1 , b2 1 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 0 , b1 1 , b2 1 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 0 , b2 0 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 0 , b2 0 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 0 , b2 1 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 0 , b2 1 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 1 , b2 0 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 1 , b2 0 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 1 , b2 1 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 0 , a3 0 , b0 1 , b1 1 , b2 1 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 1 , a3 0 , b0 0 , b1 0 , b2 0 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 1 , a3 0 , b0 0 , b1 0 , b2 0 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 1 , a3 0 , b0 0 , b1 0 , b2 1 , b3 0 ,
##  Cin 0 , a0 0 , a1 0 , a2 1 , a3 0 , b0 0 , b1 0 , b2 1 , b3 1 ,
##  Cin 0 , a0 0 , a1 0 , a2 1 , a3 0 , b0 0 , b1 1 , b2 0 , b3 0 ,


# Given a dictionary of "meanings" for the signals in a form we can use this reify() function to
# convert the form into a name-free form.

def reify(meaning, form):
  if isinstance(form, basestring):
    return meaning[form]
  return tuple(reify(meaning, inner) for inner in form)


##  for M in all_meanings(adder.values()):
##    for output_signal in sorted(adder):
##      print output_signal, int(mark(reify(M, adder[output_signal]))), ',',
##    print
##      
##  >>> 
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 0 , Sum3 0 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 0 , Sum3 1 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 1 , Sum3 0 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 1 , Sum3 1 ,
##  Carry 0 , Sum0 0 , Sum1 1 , Sum2 0 , Sum3 0 ,
##  Carry 0 , Sum0 0 , Sum1 1 , Sum2 0 , Sum3 1 ,
##  Carry 0 , Sum0 0 , Sum1 1 , Sum2 1 , Sum3 0 ,
##  Carry 0 , Sum0 0 , Sum1 1 , Sum2 1 , Sum3 1 ,
##  Carry 0 , Sum0 1 , Sum1 0 , Sum2 0 , Sum3 0 ,
##  Carry 0 , Sum0 1 , Sum1 0 , Sum2 0 , Sum3 1 ,
##  Carry 0 , Sum0 1 , Sum1 0 , Sum2 1 , Sum3 0 ,
##  Carry 0 , Sum0 1 , Sum1 0 , Sum2 1 , Sum3 1 ,
##  Carry 0 , Sum0 1 , Sum1 1 , Sum2 0 , Sum3 0 ,
##  Carry 0 , Sum0 1 , Sum1 1 , Sum2 0 , Sum3 1 ,
##  Carry 0 , Sum0 1 , Sum1 1 , Sum2 1 , Sum3 0 ,
##  Carry 0 , Sum0 1 , Sum1 1 , Sum2 1 , Sum3 1 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 1 , Sum3 0 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 1 , Sum3 1 ,
##  Carry 0 , Sum0 0 , Sum1 0 , Sum2 0 , Sum3 1 ,
##  Carry 1 , Sum0 0 , Sum1 0 , Sum2 0 , Sum3 0 ,

# In order to ease our understanding let's create a function that creates an
# integer out of a sequence of signal values (taken from B.)

def int_from_bits(*bits):
  return sum(2**n for n, bit in enumerate(reversed(bits)) if not bit)


output_signal_names = 'Carry Sum0 Sum1 Sum2 Sum3'.split()


def format_inputs(a0, a1, a2, a3,
             b0, b1, b2, b3,
             Cin):
  print ''.join(str(int(not flag)) for flag in (a0, a1, a2, a3)),
  print ''.join(str(int(not flag)) for flag in (b0, b1, b2, b3))
  return (
    int_from_bits(a0, a1, a2, a3),
    int_from_bits(b0, b1, b2, b3),
    int(not bool(Cin)),
    )


def format_outputs(Carry, Sum0, Sum1, Sum2, Sum3):
  return int_from_bits(Sum0, Sum1, Sum2, Sum3), 4 * int(not bool(Carry))


print 'a   b  Cin sum carry'

for M in all_meanings(adder.values()):
  a, b, Cin = format_inputs(**M)
##  print M
  res = dict(
    (output_signal, reduce_(reify(M, adder[output_signal])))
    for output_signal in output_signal_names
    )
##  print res
  sum_, carry = format_outputs(**res)
  print b, '+', a, '+', Cin,
  print '=', sum_, '+', carry
  print

