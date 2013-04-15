from egg import assoc, reify, walk


def unify(u, v, s):
  """
  Find substitution so that u == v while satisfying s

  >>> unify((1, x), (1, 2), {})
  {x: 2}

  """
  u = walk(s, u)
  v = walk(s, v)
  if u == v:
    return s
  if isinstance(u, basestring):
    return assoc(s, u, v)
  if isinstance(v, basestring):
    return assoc(s, v, u)
  if isinstance(u, tuple) and isinstance(v, tuple):
    if len(u) != len(v):
      return False
    for uu, vv in zip(u, v):  # avoiding recursion
      s = unify(uu, vv, s)
      if s == False: # (instead of a Substitution object.)
        break
    return s
  return False


def check(goal, rules):
  for rule in rules:
    s = unify(rule[0], goal, {})
    if s != False: # as opposed to an empty dict.
      # Proc head matches.
      return s, rule[1:]


def grind(out, goals, rules):
  S = {}
  while goals:
    goal = goals.pop(0)
    s, rule_body = check(goal, rules)
    if rule_body:
      goals.extend(rule_body)
      goals = [reify(s, goal) for goal in goals]
    S.update(s)
  return reify(S, out)


if __name__ == '__main__':
  a = 'append', (), 'x', 'x'

  p = 'append', ('cons', 'x', 'y'), 'z', ('cons', 'x', 'u')
  u = 'append',        'y',         'z',        'u'

  g = 'append', ('cons', 'a', ()), ('cons', 'b', ()), 'v'


  Rules = [(a,), (p, u)]
  goals = [g]


  print grind('v', goals, Rules)
