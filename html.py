#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The interface of this HTML generation class is pretty directly based on
# https://pypi.python.org/pypi/html but it uses ElementTree to render the
# HTML output.
#
#    Copyright © 2013 Simon Forman
#
#    This file is part of Xerblin.
#
#    Xerblin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Xerblin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Xerblin.  If not, see <http://www.gnu.org/licenses/>.
#
from xml.etree.ElementTree import Element, SubElement, tostringlist


class HTML(object):

  def __init__(self, element=None):
    if element is None:
      element = Element('html')
    assert isinstance(element, Element), repr(element)
    self.root = self.element = element

  def __getattr__(self, tag):
    e = HTML(SubElement(self.element, tag))
    e.root = self.root
    return e

  def __iadd__(self, other):
    return self._append(self.element, other)

  def _append(self, to, other):
    if isinstance(other, basestring):
      if len(to):
        last = to[-1]
        if last.tail is None:
            last.tail = other
        else:
            last.tail += other
      elif to.text is None:
        to.text = other
      else:
        to.text += other
    elif isinstance(other, Element):
      to.append(other)
    elif isinstance(other, HTML):
      if other.root is self.root:
        raise ValueError('What are you doing? No recursive HTML.')
      to.append(other.element)
    else:
      raise ValueError('Must only add strings or Elements not %r'
                       % (other,))
    return self

  def __call__(self, *content, **kw):
    for it in content:
      self._append(self.element, it)
    self.element.attrib.update((k.rstrip('_'), v) for k, v in kw.iteritems())
    return self

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_tb):
    pass

  def __repr__(self):
    return '<HTML:%r 0x%x>' % (self.element, id(self))

  def _stringify(self, encoding='us-ascii'):
    return tostringlist(self.element, method='html', encoding=encoding)

  def __str__(self):
    return ''.join(self._stringify())

  def __unicode__(self):
    return u''.join(self._stringify('UTF-8'))

  def __iter__(self):
    return iter(self._stringify())


if __name__ == '__main__':
  ht = HTML()
  with ht.head as h:
    h.title('Bananas')
  print ht
