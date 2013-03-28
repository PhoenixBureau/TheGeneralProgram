#!/usr/bin/env python
from omgebt import encode, decode, _s


for form in (
  (),
  ((),),
  (((),),),
  ((), (),),
  ((), ((),),),
  ((((),),),),
  ):
  print _s(form), '->', encode(*form)
  print '~' * 39

