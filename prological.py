# -*- coding: utf-8 -*-
from egg import nor, solve, s

#        ( ¬a ∨ ¬b )      ≡        ¬( a ∧ b )
# or_(nor('a'), nor('b')) == nor(and_('a', 'b'))
#
# True
# In the circlang they are both: (((a)(b)))
# No love for De Morgan...  Sorry dude.
#
# c0 = or_(nor(nor('mortal')), nor('human'))

# c0 = nor(and_(nor('mortal'), 'human'))


print "All humans are mortal, a.k.a. mortal OR NOT human,"
print 'IF NOT mortal THEN NOT human (Sorry, "The Highlander".)'
print
print "E = nor('mortal'), 'human'"
print

E = nor('mortal'), 'human'

#E = nor('mammal'), 'hairy', 'lactates', 'live-birth'
E = 'hairy', 'lactates', 'live-birth'


no, yes = solve(E)


print 'Look for acceptable solutions'
for m, r in yes:
  print s(r), '->', m
print


print 'Look for counter examples'
for m, r in no:
  print s(r), '->', m
print

##  ((◎(◎))) -> 1 {'human': ((),), 'mortal': ((),)}
##  ((○(◎))) -> 1 {'human': ((),), 'mortal': ()}
##  ((◎◎)) -> 0 
##  ((○◎)) -> 1 {'human': (), 'mortal': ()}
##
#    Non-human immortals;
#    Non-human mortals;
#    Human mortals;
#
#    but NO human immortals



##  for m, r in exhaust(and_(*'abcde')):
##    v = mark(r)
##    print s(r), '->', int(v), m if v else ''
