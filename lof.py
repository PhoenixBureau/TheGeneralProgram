#!/usr/bin/env python
from itertools import imap as lazy_apply, ifilter
from each_way import each_way, each_way_r
'''

"The Laws of Form" by G. Spencer-Brown.


In Python, let "a form" be any data-structure composed entirely of tuples.

We shall consider the absence of any form to be "the ground" and have the
Boolean value of True.

A "mark" is the empty tuple or any tuple without a mark, marks have the
Boolean value of False.

'''

#: The lambda function "mark" reduces any form and returns its Boolean value.
#:
mark = lambda form: not form or not any(lazy_apply(mark, form))


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


# I can haz maths?

def form_to_number(form):
  return sum(mark(inner) for inner in form)

def number_to_form(n):
  return ((),) * n


def walk(name, meaning):
    while name in meaning:
      name = meaning[name]
    return name


def reify(form, meaning):
  if form in meaning:
    return walk(form, meaning)
  return tuple(reify(inner, meaning) for inner in form)


if __name__ == '__main__':
  
  N = dict(
    (number_to_form(i), i)
    for i in range(20)
    )
  J = {(): z, ((),): y}
  j = {(): 'wrap', ((),): 'copy'}


  print 'Reify some forms into numbers.'

  for expected, form in (

    ( True, (),),
    (False, ((),),),
    ( True, (((),),),),
    (False, ((((),),),),),
    ( True, (((((),),),),),),
    (False, ((((((),),),),),),),
    ( True, (((((((),),),),),),),),
    (False, ((((((((),),),),),),),),),

    (False, ((), ())),
    (False, ((), (), ())),
    (False, ((), (), (), ())),
    (False, ((), ((), ()))),
    (False, (((),), ())),

    ( True, (((),), ((),))),
    ( True, (((),), ((),), ((),))),
    ( True, (((),), ((),), ((),), ((),))),
    ( True, (((),), ((),), ((),), ((),), ((),))),
    ( True, (((),), ((), ()), ((),), ((),))),
    ( True, (((),), ((), ((),)), ((),), ((),))),

    (False, (((),), (((),), ((),)), ((),), ((),))),
    (False, (((),), (((),),))),
    (False, (((),), (((),),), ((),), ((),),),),
    ( True, (((), ((), ())), ((((),),), ((),),),),),

    (False, ((((),),),),),
    (False, ((((),),), ((),),),),
    (False, ((((),),), (((),),), (((),),),),),
    ( True, (((((),),),), ((((),),),), ((((),),),),),),
    ):

    #print '%-5s := %s' % (('--', ())[mark(form)], form)
    print form, '->', reify(form, N)
    assert bool(R(form)) != mark(form)

  print
  print 'Create a very simple one-dimensional cellular automata.'

  # Create a small random initial form.
  form = T(T(I()))

  # Run the generation loop a few times
  for _ in range(3):

    # Reify the form with the meaning of generator functions to produce
    # a sequence of transformations to apply to the form.
    new_program = reify(form, J)

    # There is a "hole" in the logic that lets a "bare" function through,
    # So we detect and protect against that here.
    if not isinstance(new_program, tuple):
      new_program = (new_program,)

    # Display the form, its Boolean value according to mark(), and a
    # display of the program.  This last is created by reifying the
    # form with a meaning of labels corresponding to the functions in the
    # "program".  You can notice the same "hole" in the logic when the
    # label ocasionally comes out as ('p', 'a', 'r', 'w') instead of
    # ('wrap',)...
    print '%-5s -> %s -> %s' % (mark(form), form, tuple(reversed(reify(form, j))))

    # "Apply" the new program to generate a new form.
    for func in new_program:
      form = func(form)

  # Display the final form.
  print '%-5s -> %s' % (mark(form), form)
