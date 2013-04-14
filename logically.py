

def unify(u, v, s):
    """
    Find substitution so that u == v while satisfying s

    >>> unify((1, x), (1, 2), {})
    {x: 2}

    """
    s = s if isinstance(s, Substitution) else Substitution(s)
    u = s.walk(u)
    v = s.walk(v)
    if u == v:
        return s
    if isinstance(u, Var):
        return s.assoc(u, v)
    if isinstance(v, Var):
        return s.assoc(v, u)
    if isinstance(u, tuple) and isinstance(v, tuple):
        if len(u) != len(v):
            return False
        for uu, vv in zip(u, v):  # avoiding recursion
            s = unify(uu, vv, s)
            if s == False: # (instead of a Substitution object.)
                break
        return s
    return False


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


class Substitution(dict):

    def reify(self, e):
        if isinstance(e, Var):
            return self.walkstar(e)
        if isinstance(e, tuple):
            return tuple(map(self.reify, e))
        return e

    def walkstar(self, key):
        key = self.walk(key)
        if isinstance(key, tuple):
            return tuple(map(self.walkstar, key))
        return key

    def walk(self, key):
        while key in self:
            key = self[key]
        return key

    def assoc(self, key, value):
        d = self.__class__(self.copy())
        d[key] = value
        return d

    def __hash__(self):
        return hash(frozenset(self.items()))



def goaleval(goal):
    if callable(goal):          # goal is already a function like eq(x, 1)
        return goal
    if isinstance(goal, tuple): # goal is not yet evaluated like (eq, x, 1)
        egoal = goalexpand(goal)
        func, args = egoal[0], egoal[1:]
        return func(*args)
    raise TypeError("Expected either function or tuple")


def goalexpand(goalt):
    f = goalt
    while isinstance(f, tuple) and len(f) >= 1:
        goalt = f
        func, args = f[0], f[1:]
        f = func(*args)
    return goalt


def earlyorder(*goals):
    """ Reorder goals to avoid EarlyGoalErrors

    All goals are evaluated.  Those that raise EarlyGoalErrors are placed at
    the end in a lallearly

    See also:
        EarlyGoalError
    """
    bad, good = groupby(earlysafe, goals)
    if not good:
        raise EarlyGoalError()
    good = tuple(good)
    if bad:
        bad.insert(0, lallearly)
        good += (tuple(bad),)
    return good


def earlysafe(goal):
    """ Call goal be evaluated without raising an EarlyGoalError """
    try:
        goaleval(goal)
        return True
    except EarlyGoalError:
        return False

class EarlyGoalError(Exception):
    pass



# Goal functions.


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
        if result:
            yield result
    return goal_eq

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

    head, tail = goals[0], (lall,) + tuple(goals[1:])

    def allgoal(s):
        g = goaleval(s.reify(head))
        return unique(interleave(
            goaleval(ss.reify(tail))(ss) for ss in g(s)
            ))

    return allgoal


# Main "interface" to the unification function.


def run(n, x, *goals, **kwargs):
    return take(
        n,
        unique(
            s.reify(x)
            for s in goaleval(lallearly(*goals)) (Substitution(kwargs))
            )
        )


# These functions are generic (in the sense that they don't have anything
# specifically to do with unification, just helping out in general.)
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


def interleave(seqs, pass_exceptions=()):
    iters = map(iter, seqs)
    while iters:
        newiters = []
        for itr in iters:
            try:
                yield next(itr)
                newiters.append(itr)
            except (StopIteration,) + tuple(pass_exceptions):
                pass
        iters = newiters


def groupby(predicate, coll):
    bins = [], []
    for item in coll:
        bins[predicate(item)].append(item)
    return bins


if __name__ == '__main__':
    x = Var('x')
    y = Var('y')
    print run(0, y, (eq, x, 5), (eq, x, y))



    u = Var('u')
    z = Var('z')
    cons = Var('cons')
    ap = Var('append')
    a = Var('a')
    b = Var('b')
    c = Var('c')
    v = Var('v')

    A = a, (), x, x
    P = a, (c, x, y), z, (c, x, u)
    U = a, y, z, u
    G = a, (c, a, ()), (c, b, ()), v


    new_G = run(0, U, (eq, P, G))
    print new_G
    print run(0, v, (eq, A, new_G))
