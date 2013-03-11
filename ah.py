from pprint import pprint
from json import dumps


MINIMUM = 7


mark = lambda form: not form or not any(map(mark, form))
depth = lambda form: 1 if not form else 1 + max(map(depth, form))
count = lambda form: 1 + sum(map(count, form))


def size(form, minimum=MINIMUM, margin=3):
  '''
  Technically radius.
  '''
  n = len(form)
  if not n:
    return minimum
  if n == 1:
    return margin + size(form[0], minimum, margin)
  sizes = sorted(map(size, form), reverse=True)
  return depth(form) * margin + sizes[0] + sizes[1]


def to_d3_graph(form, rank=1, max_depth=None):
  if max_depth is None:
    max_depth = depth(form)
  d = {
    'name': str(id(form)),
    'mark': mark(form),
    }
  if form:
    d['children'] = map(lambda f: to_d3_graph(f, rank + 1, max_depth), form)
    if len(form) == 1:
      d['children'].append(to_d3_graph((), rank + 1, max_depth))
    d['size'] = MINIMUM * count(form)
  else:
    d['size'] = MINIMUM * max_depth / rank
  return d


def to_d3_json(form, nodes=None, links=None):

  if nodes is None:
    nodes = []
  if links is None:
    links = []

  d = {
    'name': str(id(form)),
    'mark': mark(form),
    'radius': size(form),
    'charge': 0, # -30 if len(form) > 1 else -1,
    'link_distance': size(form) * 2 / 3 if len(form) > 1 else 0,
    }

  nodes.append(d)

  if form:
    links.extend(
      (d, child)
      for child in map(lambda f: to_d3_json(f, nodes, links), form)
      )

  return d


form = tuple(
  tuple(() for _ in range(n))
  for n in range(24)
  )
##
##(
##  (((),),(),),
##  (),
##  (
##    ((((),),(),(),()),),
##    (),((),),
##    ),
##  (
##    ((((),),(),(),),),
##    (),(((),),),
##    ),
##  (
##    ((((),),(),(),),),
##    (),((),),
##    ),
##  ) # ((((),(),),),(),),(),)

print dumps(to_d3_graph(form), indent=2)


##for f in (form,) + form:
##  print len(f), count(f), depth(f), f



##
##N, L = [], []
##to_d3_json(form, N, L)
##
##rev = dict((id(f), i) for i, f in enumerate(N))
##
##L = [{
##  'source': rev[id(d)],
##  'target': rev[id(child)],
##  'link_distance': d['link_distance'],
##  } for d, child in L]
##
##print dumps({'nodes': N, 'links': L}) # , indent=2)
##
##
##
