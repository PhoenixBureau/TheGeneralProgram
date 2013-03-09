from sys import stderr
from random import choice


def each_way(a=None, b=None):
  if a is b is None:
    return ((),), ((), ())
  if b is None:
    return ((a,),), ((a,), ())
  if a is None:
    return ((), b), ((), (b,))
  return ((a,), b), ((a,), (b,))


def each_way_r(meta_form):
  for form in meta_form:

    if form == (((),), ((), ())): # a = b = nothing
      continue # yield nothing

    try: # Both a and b are something
      (((la,), lb), ((ra,), (rb,))) = form
      yield la if la == ra and lb == rb else form
    except  ValueError:

      try: # b is nothing
        ((la,),), ((ra,), rb) = form
        yield la if la == ra and rb == () else form
      except ValueError:

        try: # a is nothing
          (la, lb), (ra, (rb,)) = form
          if not la == ra == (): # the a's must be () i.e. nothing in ().
            raise ValueError
          # yield nothing
        except ValueError:

          yield form


def generate(source_set):
  source_set = tuple(source_set)
  return each_way(choice(source_set), choice(source_set))


q = set((None, ())) # start with nothing and something.


def increase():
  while True:
    new = generate(q)
    if new not in q:
      print >> stderr, new
      q.add(new)
      break


if __name__ == '__main__':
  trial = (
    each_way(),
    each_way('a'),
    each_way(b='b'),
    each_way('a', 'b'),
    )

  for l, r in trial:
    print l, r
  print

  print tuple(each_way_r(trial))

