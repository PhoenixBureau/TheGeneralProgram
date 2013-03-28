# -*- coding: utf-8 -*-

#: Depth-first encoding of forms.
encode = lambda *f: '1' + encode(*f[0]) + encode(*f[1:]) if f else '0'


#: Decode paths from encoder.
decode = lambda path: _decode(iter(path))[0]


def _decode(path):
  if next(path) == '0':
    return (), path
  A, path = _decode(path)
  B, path = _decode(path)
  return (A,) + B, path


def _s(shell):
  return (
    ''.join(map(str, shell))
      .replace(',', '')
      .replace(' ', '')
      .replace('(())', '◎')
      .replace('()', '○')
    )

if __name__ == '__main__':

  a = ()
  b = ((),)
  c = (((),),)
  d = (((),),(), )
  e = ((), ((),))
  FO = (a, b, c, d, e)
  for shell in FO:
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
  for shell in FO:
    shell = (shell,) * 2
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
  for shell in FO:
    shell = (shell,) * 3
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
