from egg import and_, implies, s, Reduce, fstan

##t = ()
##U = {t: t}
##get = U.setdefault
##cache = lambda form: get(form, form)
##
##print t is cache(t)
##
##v = cache(((),))


a, b, c = 'abc'

# (a -> b and b -> c) -> (a -> c)

A = implies(
  and_(implies(a, b), implies(b, c)),
  implies(a, c)
  )

statement = tuple(Reduce(A))

print s(A)
print s(statement)
print () == fstan(A) == fstan(statement)

