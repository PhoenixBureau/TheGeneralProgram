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

##
##  verbose_run(tuple(prepare_program((
##
##      ('wrap', 0),
##      ('wrap', 0),
##      ('wrap', 0),
##      ('wrap', 0),
##
##      ))))
##
##  verbose_run(tuple(prepare_program((
##
##      ('wrap', 0),
##      ('wrap', 1),
##      ('wrap', 2),
###      ('wrap', 0),
##
##      ))))
##
##  verbose_run(tuple(prepare_program((
##
##      ('wrap', 0),
##      ('wrap', 1),
##      ('wrap', 0),
##      ('copy', 0),
##
##      ))))
##
##  verbose_run(tuple(prepare_program((
##
##      ('wrap', 0),
##      ('undelete', 0, 0, 0),
##      ('wrap', 0, 3),
##
##      ))))
##
##  print 'Reify some forms into numbers.'
##
##  for expected, form in (
##
##    ( True, (),),
##    (False, ((),),),
##    ( True, (((),),),),
##    (False, ((((),),),),),
##    ( True, (((((),),),),),),
##    (False, ((((((),),),),),),),
##    ( True, (((((((),),),),),),),),
##    (False, ((((((((),),),),),),),),),
##
##    (False, ((), ())),
##    (False, ((), (), ())),
##    (False, ((), (), (), ())),
##    (False, ((), ((), ()))),
##    (False, (((),), ())),
##
##    ( True, (((),), ((),))),
##    ( True, (((),), ((),), ((),))),
##    ( True, (((),), ((),), ((),), ((),))),
##    ( True, (((),), ((),), ((),), ((),), ((),))),
##    ( True, (((),), ((), ()), ((),), ((),))),
##    ( True, (((),), ((), ((),)), ((),), ((),))),
##
##    (False, (((),), (((),), ((),)), ((),), ((),))),
##    (False, (((),), (((),),))),
##    (False, (((),), (((),),), ((),), ((),),),),
##    ( True, (((), ((), ())), ((((),),), ((),),),),),
##
##    (False, ((((),),),),),
##    (False, ((((),),), ((),),),),
##    (False, ((((),),), (((),),), (((),),),),),
##    ( True, (((((),),),), ((((),),),), ((((),),),),),),
##    ):
##
##    #print '%-5s := %s' % (('--', ())[mark(form)], form)
##    print form, '->', reify(form, N)
##    assert bool(R(form)) != mark(form)
##
##  print
##  print 'Create a very simple one-dimensional cellular automata.'
##
##  # Create a small random initial form.
##  form = T(T(I()))
##
##  # Run the generation loop a few times
##  for _ in range(3):
##
##    # Reify the form with the meaning of generator functions to produce
##    # a sequence of transformations to apply to the form.
##    new_program = reify(form, J)
##
##    # There is a "hole" in the logic that lets a "bare" function through,
##    # So we detect and protect against that here.
##    if not isinstance(new_program, tuple):
##      new_program = (new_program,)
##
##    # Display the form, its Boolean value according to mark(), and a
##    # display of the program.  This last is created by reifying the
##    # form with a meaning of labels corresponding to the functions in the
##    # "program".  You can notice the same "hole" in the logic when the
##    # label ocasionally comes out as ('p', 'a', 'r', 'w') instead of
##    # ('wrap',)...
##    print '%-5s -> %s -> %s' % (mark(form), form, tuple(reversed(reify(form, j))))
##
##    # "Apply" the new program to generate a new form.
##    for func in new_program:
##      form = func(form)
##
##  # Display the final form.
##  print '%-5s -> %s' % (mark(form), form)
