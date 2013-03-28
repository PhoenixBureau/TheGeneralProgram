from pprint import pprint
from lof import (
  wrap,
  unwrap,
  copy,
  uncopy,
  delete,
  undelete,
  apply_,
  )


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
found = generate(('a', 'b', 'c'), steps, forms)


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


for k, v in sorted(Programs.items()):
  print k
  pprint(v)
  print

##k = Programs.values()
##J = [(len(l), count(l), depth(l), l) for l in k]
##J.sort()
##print '\n'.join(
##  ('%-3i %-3i %-3i %r' % (l, c, d, form))
##  for l, c, d, form in J
##  )

