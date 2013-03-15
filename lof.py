#!/usr/bin/env python
from itertools import imap, ifilter
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


def delete(form, i):
  '''
  OA -> O
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + form[i + 1:]


def undelete(form, i, anything):
  '''
  O -> OA
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + (anything,) + form[i:]


def copy(form, i):
  '''
  A(B) -> A(AB)
  '''
  left, A, t, right = form[:i + 1], form[i], form[i + 1], form[i + 2:]
  return left + ((A,) + t,) + right


def uncopy(form, i):
  '''
  A(AB) -> A(B)
  '''
  left, A, t, right = form[:i], form[i], form[i + 1], form[i + 2:]
  assert t[0] == A
  return left + (t[1:],) + right


def apply_(form, program):
  if program and callable(program[0]):
    function, args = program[0], program[1:]
    return function(form, *args)
  for inner in program:
    form = apply_(form, inner)
  return form


Instructions = {
  ((number_to_form(1),),): wrap,
  ((number_to_form(2),),): unwrap,
  ((number_to_form(3),),): delete,
  ((number_to_form(4),),): undelete,
  ((number_to_form(5),),): copy,
  ((number_to_form(6),),): uncopy,
  }


Instructions_reversed = {
  'wrap': ((number_to_form(1),),),
  'unwrap': ((number_to_form(2),),),
  'delete': ((number_to_form(3),),),
  'undelete': ((number_to_form(4),),),
  'copy': ((number_to_form(5),),),
  'uncopy': ((number_to_form(6),),),
  }


def prepare_program(program):
  return tuple(
    (Instructions_reversed[instr], number_to_form(index))
    for instr, index in program)


N = dict(
  (number_to_form(i), i)
  for i in range(20)
  )
meaning = {}
meaning.update(N)
meaning.update(Instructions)


def verbose_run(program):
  print '---\nRaw program as a form expression:'
  for instruction, selector in program:
    print (instruction, selector)

  print '---\nHuman friendly form:'
  for instruction, selector in reify(program, meaning):
    print (instruction.__name__, selector)

  print '---\nRun the program on the () form:'

  print apply_((), reify(program, meaning))
  print '---'


if __name__ == '__main__':

  verbose_run(prepare_program((

      ('wrap', 0),
      ('wrap', 0),
      ('wrap', 0),
      ('wrap', 0),

      )))

  verbose_run(prepare_program((

      ('wrap', 0),
      ('wrap', 1),
      ('wrap', 2),
#      ('wrap', 0),

      )))

  verbose_run(prepare_program((

      ('wrap', 0),
      ('wrap', 1),
      ('wrap', 0),
      ('copy', 0),

      )))

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
