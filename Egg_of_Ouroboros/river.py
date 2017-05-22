

Mark = ()
Void = Mark,


def solve(form, marks):
  '''
  Given a form and a set of names that are Marks assume all other names
  in the form are Void and reduce to basic value (Mark or Void.)
  '''
  for inner in form:
    if isinstance(inner, basestring):
      if inner in marks:
        return Void
    elif not solve(inner, marks):
      return Void
  return Mark


def opposite(a, b): return (a, (b,)), ((a,), b)
def same(a, b): return opposite(a, b),


# Build simple "programs" that just flip the passed-in signal names.
_flip = lambda *signals: {s: (s,) for s in signals}


U = m, w, g, c = 'mwgc'


S = (

  # If the man and the wolf are on the same side and the goat and the
  # cabbage are on opposite sides, it is safe for the man to ferry the
  # wolf.
  ((same(m, w), opposite(g, c)), _flip(m, w)),

  # If the man and the goat are on the same side of the river he can
  # ferry the goat.  (The cabbage and wolf can be on either side.)
  ((same(m, g),), _flip(m, g,)),

  # If the man and the cabbage are on the same side and the goat and wolf
  # are on opposite sides he can ferry the cabbage.
  ((same(m, c), opposite(g, w)), _flip(m, c)),

  # Any time the goat is on one side and the wolf and the cabbage are on
  # the other the man can safely cross the river by himself, without any
  # of the others (and he's probably well glad for the respite.)
  ((opposite(g, w), opposite(g, c)), _flip(m)),
  )


# Everyone starts on one side of the river,
R = set()


# ...and the goal is to get to the other side.
Target = {m, w, g, c}


# Remember the available candidate moves for each state.
states = {}


# Remember the order in which we found multiple moves to attempt.
stack = []


# Keep track of the previous step (so we don't just undo it.)
prev = None


print ''.join(sorted(U))


# A little visual aid to see the state of the puzzle.
_view = lambda r, u: ''.join('_O'[n in r] for n in sorted(u))


while R != Target:
  print _view(R, U)

  state = frozenset(R) # Because you can't hash sets.

  try:
    C = states[state]
  except KeyError:
    # Check the current state against the rules' expressions
    # to find all the applicable "ways forward".
    C = states[state] = [
      program
      for expression, program in S
      if not program is prev # each rule is reversible,
                             # don't undo our previous step.
      and not solve(expression, R)
      ]

  # What if we hit a dead-end?
  while not C: # check the stack for other things to try...
    try:
      R, C = stack.pop()
    except IndexError:
      # Nothing left? We can't solve this puzzle.
      raise Exception("NOOOO")
    print 'backtracking to', _view(R, U), C
    # Note that if this C has been emptied in the meantime
    # we will loop and keep looking.

  # Pick the next possible step.
  P = prev = C.pop(0)

  # If there are still more possibilities, remember them.
  if C:
    stack.append((R, C))
    print 'remembering', _view(R, U), C

  # To calculate the new R first collect all the signals in R that are
  # marks but that are not mentioned in the current P (and so cannot be
  # set to Void by it) then add the marks generated by solving P's
  # expressions with the marks in R.
  R = R.difference(P).union(
    signal
    for signal, expression in P.iteritems()
    if not solve(expression, R)
    )

print _view(R, U)