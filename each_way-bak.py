
def each_way(form):
  try:
#    (((la,), lb), ((ra,), (rb,))) = form

    left, right = two(form)
    la, lb = two(left)
    la = q(la)

    ra, rb = two(right)
    ra, rb = q(ra), q(rb)

  except ValueError:
    return form
  return la if la == ra and lb == rb else form

(((la,), lb), ((ra,), (rb,)))

a = (('a',), 'b'), (('a'), ('b'))

##for test in (
##  a,
## ( ((), 'b'), ((), ('b')) ),
## ( (('a',),), (('a'), ()) ),
## ( ((),), ((), ()) ),
##  ):
##  print test
##  try:
##    print each_way(test)
##  except ValueError:
##    print 'failed'
##  print '~' * 70


(((),), ((), ()))

#(((_),_), ((_), (_)))

'''

(               )
 (   )  (      ) 
  ()     ()  ()  


((a)b)((a)(b))


((a))((a)())


(()b)(()(b))


(())(()())

(l)(r0 r1)


'''

##try:
##  left, right = form
  
def make_each_way(a, b):
  return (((a,), b), ((a,), (b,)))


D = (), ((),)

print make_each_way('a', 'b')
print

from itertools import imap as lazy_apply, ifilter
mark = lambda form: not form or not any(lazy_apply(mark, form))

d = make_each_way((), ())
z = make_each_way(d, d)
print z
print
print

for a in D:
  for b in D:
    p = make_each_way(a, b)
    print '%s %s -> %s' % (a, b, p)
    print each_way(p)
    print mark(p), bool(each_way(p))
    print
