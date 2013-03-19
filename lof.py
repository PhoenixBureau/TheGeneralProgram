#!/usr/bin/env python
import sys
from pprint import pprint
from collections import defaultdict
from itertools import imap, ifilter
from functools import wraps
from each_way import each_way, each_way_r
'''

"The Laws of Form" by G. Spencer-Brown.


In Python, let "a form" be any data-structure composed entirely of tuples.

We shall consider the absence of any form to be "the ground" and have the
Boolean value of True.

A "mark" is the empty tuple or any tuple without a mark; marks have the
Boolean value of False.

'''

#: The lambda function "mark" reduces any form and returns its Boolean value.
#:
mark = lambda form: not form or not any(imap(mark, form))


#  Reduce a form according to these rules:
#
#    (()) -> nothing    "Cancel"
#    ()() -> ()      un-"Repeat"
#


#: Let a be a Value-Preserving function that removes (()) from forms.
#:
#: This corresponds to applying "Cancel" to all possible inner forms in a
#: form.
#:
a = lambda form: tuple(inner for inner in form if inner != ((),))

#: Let b be a Value-Preserving function that removes all copies of () in
#: a form.
#:
#: This corresponds to applying un-"Repeat" to all possible inner forms
#: in a form.
#:
b = lambda form: form if () not in form else ((),) + tuple(ifilter(None, form))


#: We can define the Value-Preserving function R in terms of recursive
#: application of the a and b reduction functions, which correspond to
#: "Cancel" and un-"Repeat" applied exhaustively.
#:
#: bool(R(form)) == not mark(form) for all forms.
#:
R = lambda form: tuple(a(b(tuple(map(R, form)))))






#  Produce new forms by applying these rules:
#
#    nothing -> (())
#         () -> ()()
#

z = lambda form: (((),),) + tuple(form)

y = lambda form: ((),) + form if () in form else form

P = lambda form: tuple(y(z(P(inner) for inner in form)))


# Generate random new forms.
from random import random

T = lambda form: z(form) if random() > 0.5 else y(form)
I = lambda: () if random() > 0.5 else ((),)


# Memo-ize for efficiency.
#
def memoize(f, memo):
  def mf(form):
    if form == (): return True
    try: return memo[form]
    except KeyError: m = memo[form] = f(form)
    return m
  return mf
D = {}
mark = memoize(mark, D)


def deep(func):
  @wraps(func)
  def f(form, *indicies):
    if len(indicies) == 1:
      return func(form, indicies[0])
    i, indicies = indicies[0], indicies[1:]
    n = f(form[i], *indicies)
    return form[:i] + (n,) + form[i + 1:]
  return f


@deep
def wrap(form, i):
  '''

  * -> ((*))

  In order to handle the wrapping of nothing in-between the inner forms
  of the form we adopt the convention that even i (0, 2, 4, ...) will
  select the intersticies of the inner forms, while the odd i (1, 3, ...)
  will select the inner forms themselves.

  Therefore the valid indicies for a form g are: range(2 * len(g) + 1).
  Greater indicies will append wrap the nothing at the end of the form.

  If you wrap (0, 1, 2) with the following indicies you get these
  resultant forms:

    0 -> (((),), 0, 1, 2)
    1 -> (((0,),), 1, 2)
    2 -> (0, ((),), 1, 2)
    3 -> (0, ((1,),), 2)
    4 -> (0, 1, ((),), 2)
    5 -> (0, 1, ((2,),))
    6 -> (0, 1, 2, ((),))

  '''
  wrap_nothing = not i % 2
  i /= 2
  left = form[:i]
  if wrap_nothing:
    right = form[i:]
    t = ((),)
  else:
    right = form[i + 1:]
    t = ((form[i],),)
  return left + (t,) + right


@deep
def unwrap(form, i):
  '''

  ((*)) -> *

  Unwrap an inner form (including nothing) in form at index i.

  (Unlike the wrap() function which handles indices specially to permit
  one function to wrap both "present" forms and intersticial nothing,
  unwrap() uses just the normal index.


    0 -> (((),), 0, 1, 2) -> (0, 1, 2)
    0 -> (((0,),), 1, 2) -> (0, 1, 2)
    1 -> (0, ((),), 1, 2) -> (0, 1, 2)
    1 -> (0, ((1,),), 2) -> (0, 1, 2)
    2 -> (0, 1, ((),), 2) -> (0, 1, 2)
    2 -> (0, 1, ((2,),)) -> (0, 1, 2)
    3 -> (0, 1, 2, ((),)) -> (0, 1, 2)

  '''
  left, t, right = form[:i], form[i], form[i + 1:]
  return (left + right) if t == ((),) else (left + (_k(t),) + right)

# Helper function to "unwrap" a single wrapped form.
_k = lambda (((anything,),)): anything


@deep
def delete(form, i):
  '''
  OA -> O
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + form[i + 1:]


def undelete(form, anything, *i):
  @deep
  def inner_undelete(form, i):
    return _undelete(form, anything, i)
  return inner_undelete(form, *i)


def _undelete(form, anything, i):
  '''
  O -> OA
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + (anything,) + form[i:]


@deep
def copy(form, i):
  '''
  A(B) -> A(AB)
  '''
  left, A, t, right = form[:i + 1], form[i], form[i + 1], form[i + 2:]
  return left + ((A,) + t,) + right


@deep
def uncopy(form, i):
  '''
  A(AB) -> A(B)
  '''
  left, A, t, right = form[:i], form[i], form[i + 1], form[i + 2:]
  assert t[0] == A
  return left + (t[1:],) + right


def apply_(form, program, indent=0):
#  print >> sys.stderr, '  ' * indent, ' '.join(str(f) for f in form)
  if program and callable(program[0]):
    function, args = program[0], program[1:]
#    print >> sys.stderr, '  ' * indent, function.__name__, args
    return function(form, *args)
  for inner in program:
    form = apply_(form, inner)
  return form


P = (
  (wrap, 0),
  (undelete, (), 0, 0),
  (wrap, 0, 3),
  )


form = apply_((), (P, P))
#print ' '.join(str(f) for f in form)


rules = '''


   (()) -> nothing
nothing -> (())

   ()() -> ()
     () -> ()()

   A(B) -> A(AB)
  A(AB) -> A(B)


'''


def generate(form, steps, seen):
  found = {}
  for step in steps:
    try:
      new_form = apply_(form, step)
      if new_form not in seen and new_form not in found:
        found[new_form] = step
        seen.add(new_form)
    except:
      pass
  return found


Programs = {}


steps = [
  (rule, i)
  for rule in (wrap, unwrap, copy, uncopy, delete)
  for i in range(5)
  ]


forms = set()
found = generate((), steps, forms)


depth = lambda form: 1 + (max(depth(inner) for inner in form) if form else 0)
count = lambda form: 1 + sum(count(inner) for inner in form)

##print len(forms)
##pprint(forms)
##
##print len(found)
##pprint(found)

def _l(step): return (step[0].__name__,) + step[1:]

for form, step1 in found.iteritems():

  Programs[_l(step1)] = form

  found = generate(form, steps, forms)
  for form, step2 in found.iteritems():

    Programs[(_l(step1), _l(step2))] = form

    found = generate(form, steps, forms)
    for form, step3 in found.iteritems():

      Programs[(_l(step1), _l(step2), _l(step3))] = form

      found = generate(form, steps, forms)
      for form, step4 in found.iteritems():

        Programs[(_l(step1), _l(step2), _l(step3), _l(step4))] = form

        found = generate(form, steps, forms)
        for form, step5 in found.iteritems():

          Programs[(_l(step1), _l(step2), _l(step3), _l(step4),
                    _l(step5))] = form

          found = generate(form, steps, forms)
          for form, step6 in found.iteritems():

            Programs[(_l(step1), _l(step2), _l(step3), _l(step4),
                      _l(step5), _l(step6))] = form

            found = generate(form, steps, forms)
            for form, step7 in found.iteritems():

              Programs[(_l(step1), _l(step2), _l(step3), _l(step4),
                        _l(step5), _l(step6), _l(step7))] = form


##for k, v in sorted(Programs.items()):
##  print k
##  pprint(v)
##  print
k = Programs.values()
J = [(len(l), count(l), depth(l), l) for l in k]
J.sort()
print '\n'.join(
  ('%-3i %-3i %-3i %r' % (l, c, d, form))
  for l, c, d, form in J
  )

