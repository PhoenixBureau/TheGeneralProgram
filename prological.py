# -*- coding: utf-8 -*-
from egg import nor, and_, or_, solve, Reduce, s


#        ( ¬a ∨ ¬b )      ≡        ¬( a ∧ b )
# or_(nor('a'), nor('b')) == nor(and_('a', 'b'))
#
# True
# In the circlang they are both: (((a)(b)))
# No love for De Morgan...  Sorry dude.
#
# c0 = or_(nor(nor('mortal')), nor('human'))

# c0 = nor(and_(nor('mortal'), 'human'))


E = ('mortal',), 'human'

#F = and_('John', 'mortal')
#G = and_('John', 'human')
#E = nor('mammal'), 'hairy', 'lactates', 'live-birth'
#E = 'hairy', 'lactates', 'live-birth'


print "All humans are mortal, a.k.a. mortal OR NOT human,"
print 'IF NOT mortal THEN NOT human (Sorry, "The Highlander".)'
print
print "E =", s(E)
print
print "     ¬ mortal ∨ human"
print


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


print '''
From Meguire 2007
Stoll’s example is in effect the following clause:

Premises:
  (CU) ⇔ ~C ∧ ~U
  (S)U ⇔ S → U
  (WP)I ⇔ (W ∨ P) → I
  (I)CS ⇔ I → (C ∨ S)

Conclusion: (W) ⇔ ~W

'''
##  A pa calculation verifying this clause goes as follows:
##
##    ((CU))((S)U)((WP)I)((I)CS)W′  Enclose premises, concatenate all.
##        CU((S)U)((WP)I)((I)CS)W′  C1
##          CU((S))((WP)I)((I)S)W′ C2,2x
##              CUS((WP)I)((I)S)W′ C1
##               CUS((WP)I)((I))W′ C2
##                   CUS((WP)I)IW′ C1
##                    CUS((WP))IW′ C2
##                        CUSWPIW′ C1
##                       W′WCUSPI  OI
##                             ()  J0.
##
# Note: *′ = (*)


# Note: I use or_() to put "bare" terms in ((*))
# i.e. (I)CS -> (((I)CS)) This is value-preserving for
# the evaluation but necessary due to Python tuple behavior.


a = 'C', 'U'
b = or_(('S',), 'U')
c = or_(('W', 'P'), 'I')
d = or_(('I',), 'C', 'S')

e = 'W',

E = and_(a, b, c, d, nor(e))
print 'E =', s(E)
E = Reduce(E)
print '**Reduce**'
print 'E =', s(E)

valid = not solve(E)[0]
print
print s(E), '->', valid




