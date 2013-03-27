from itertools import combinations_with_replacement as combo, chain, permutations
from another_lof_game import a


initial = (), ((),)
K = set(initial)
Found = K.copy()


def permute(n, k=K):
  return set(chain(*(permutations(form) for form in set(combo(k, n)))))


def foo(n, root, extended):
  extended = extended.copy()
  extended.update(permute(n, k=root))
  extended.update(permute(n, k=extended))
  return extended

print 'building forms...'
T = foo(2, K, Found)
TH = foo(3, K, Found)

Found.update(T)
Found.update(TH)

T = foo(2, K, Found)
TH = foo(3, K, Found)

Found.update(T)
Found.update(TH)

print 'done, sorting then printing...'
for form in sorted(Found):
  print form
  print a(form)

##for form in sorted(permute(3)):
##  print form
##print '-'
##
##for form in sorted(permute(4)):
##  print form
##print '-'
##print '-'
##
##Found.update(permute(2))
##for form in sorted(Found):
##  print form
##print '-'
##
##Found.update(permute(2, k=Found))
##for form in sorted(Found):
##  print form
##print '-'
##



