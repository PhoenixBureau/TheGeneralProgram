from egg import *


def convert(form):
  if isinstance(form, basestring):
    return form
  return frozenset(convert(inner) for inner in form)
