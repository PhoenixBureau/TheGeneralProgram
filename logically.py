
def run(n, x, *goals, **kwargs):
    return take(n, unique(reify(x, s) for s in goaleval(lallearly(*goals))({})))

import itertools as it
def take(n, seq):
    if n is None:
        return seq
    if n == 0:
        return tuple(seq)
    return tuple(it.islice(seq, 0, n))

def unique(seq):
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item

def reify(e, s):
    if isvar(e):
        return walkstar(e, s)
    elif isinstance(e, tuple):
        return tuple(reify(arg, s) for arg in e)
    else:
        return e

def walkstar(key, d):
    key = transitive_get(key, d)
    if isinstance(key, tuple):
        return tuple(map(lambda k: walkstar(k, d), key))
    else:
        return key

def transitive_get(key, d):
    while key in d:
        key = d[key]
    return key
walk = transitive_get

def goaleval(goal):
    if callable(goal):          # goal is already a function like eq(x, 1)
        return goal
    if isinstance(goal, tuple): # goal is not yet evaluated like (eq, x, 1)
        egoal = goalexpand(goal)
        return egoal[0](*egoal[1:])
    raise TypeError("Expected either function or tuple")

def goalexpand(goalt):
    tmp = goalt
    while isinstance(tmp, tuple) and len(tmp) >= 1 and not callable(tmp):
        goalt = tmp
        tmp = goalt[0](*goalt[1:])
    return goalt

def lallearly(*goals):
    """ Logical all with goal reordering to avoid EarlyGoalErrors

    See also:
        EarlyGoalError
        earlyorder
    """
    return (lall,) + tuple(earlyorder(*goals))

def lall(*goals):
    """ Logical all

    >>> from logpy import lall, membero
    >>> g = lall(membero(x, (1,2,3), membero(x, (2,3,4))))
    >>> tuple(g({}))
    ({x: 2}, {x: 3})
    """
    if not goals:
        return success
    if len(goals) == 1:
        return goals[0]
    def allgoal(s):
        g = goaleval(reify(goals[0], s))
        return unique_dict(interleave(
            goaleval(reify((lall,) + tuple(goals[1:]), ss))(ss)
            for ss in g(s)))
    return allgoal

def earlyorder(*goals):
    """ Reorder goals to avoid EarlyGoalErrors

    All goals are evaluated.  Those that raise EarlyGoalErrors are placed at
    the end in a lallearly

    See also:
        EarlyGoalError
    """
    groups = groupby(earlysafe, goals)
    good = groups.get(True, [])
    bad  = groups.get(False, [])

    if not good:
        raise EarlyGoalError()
    else:
        if not bad:
            return tuple(good)
        else:
            return tuple(good) + ((lallearly,) + tuple(bad),)

def dicthash(d):
    return hash(frozenset(d.items()))

def unique_dict(seq):
    seen = set()
    for d in seq:
        h = dicthash(d)
        if h not in seen:
            seen.add(h)
            yield d

def interleave(seqs, pass_exceptions=()):
    iters = it.imap(iter, seqs)
    while iters:
        newiters = []
        for itr in iters:
            try:
                yield next(itr)
                newiters.append(itr)
            except (StopIteration,) + tuple(pass_exceptions):
                pass
        iters = newiters

def earlysafe(goal):
    """ Call goal be evaluated without raising an EarlyGoalError """
    try:
        goaleval(goal)
        return True
    except EarlyGoalError:
        return False

class EarlyGoalError(Exception):
    pass

def groupby(f, coll):
    d = dict()
    for item in coll:
        key = f(item)
        if key not in d:
            d[key] = []
        d[key].append(item)
    return d

def fail(s):
    return ()

def success(s):
    return (s,)

def eq(u, v):
    """ Goal such that u == v

    See also:
        unify
    """
    def goal_eq(s):
        result = unify(u, v, s)
        if result is not False:
            yield result
    return goal_eq

def unify(u, v, s):  # no check at the moment
    """ Find substitution so that u == v while satisfying s

    >>> unify((1, x), (1, 2), {})
    {x: 2}
    """
    u = walk(u, s)
    v = walk(v, s)
    if u == v:
        return s
    if isvar(u):
        return assoc(s, u, v)
    if isvar(v):
        return assoc(s, v, u)
    if isinstance(u, tuple) and isinstance(v, tuple):
        if len(u) != len(v):
            return False
        for uu, vv in zip(u, v):  # avoiding recursion
            s = unify(uu, vv, s)
            if s is False:
                return False
        return s
    return False

def assoc(dict, key, value):
    d = dict.copy()
    d[key] = value
    return d

class Var(object):

    _id = 1

    def __init__(self, *token):
        if not token:
            token = "_%s" % self._id
            self._id += 1

        elif len(token) == 1:
            token = token[0]

        self.token = token

    def __str__(self):
        return "~" + str(self.token)
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.token == other.token

    def __hash__(self):
        return hash((type(self), self.token))

isvar = lambda t: isinstance(t, Var)

x = Var('x')
y = Var()
print run(0, y, (eq, x, 5), (eq, x, y))









