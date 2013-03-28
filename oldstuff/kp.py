from functools import wraps

def deep(func):
  @wraps(func)
  def f(form, *indicies):
    if len(indicies) == 1:
      return func(form, indicies[0])
    i, indicies = indicies[0], indicies[1:]
    return f(form[i], *indicies)
  return f
