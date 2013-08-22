# -*- coding: utf-8 -*-
from html import HTML


nbsp = u'\xa0'


def index(ht=None, blocks=()):

  if ht is None: ht = HTML()

  with ht.head as h:
    h.title('The Egg of Ouroboros Web Site')
    h.meta(charset='utf-8')
    h.link(
      href='http://fonts.googleapis.com/css?family=EB+Garamond|Muli:400,300',
      rel='stylesheet',
      type_='text/css',
      )
    h.link(href='site.css', rel='stylesheet', type_='text/css')

  with ht.body as b:
    for block in blocks:
      d = b.div(class_="prose")
      block(d)
      b.hr

  return ht


def first(d):
  d.h1('The Egg of Ouroboros', align="center")
  d.h3('A Notation for Tractable Reasoning', align="center")
  separator(d)

  d.blockquote('In the beginning was the Void, and the Void was without Form.')

  d.p('''There are three rewards to be won by eating the Egg of Ouroboros.''')
  d.p('''The first and most important (indeed the only import) is to effect transcendence of the illusion of form.''')
  d.p('''The second is a notation for universal reasoning that is simple, elegant and direct.  This notation provides a mechanism for constructing all possible universes and, therefore, our own.  It is the power of this notation to permit the prepared mind to approach math as scripture and read the Word of God in the Libre Mundi.''')
  d.p('''Third, new results in circuit design and program construction are enabled.''')

  separator(d)

  d.p('''Over the last century a small group of researchers, working largely independently and in isolation, have discovered and refined the Universal Language.''')
  d.p('''It is a logic-symbolic notation, not a spoken language (i.e. not like Esperanto), that captures and expresses the essence of logical reasoning in a direct and very powerful way.''')
  p = d.p('''The rules of logical reasoning (and Set Theory, etc.) expressed in the Universal Language admit of a ''')
  p.a('decision procedure', href="https://en.wikipedia.org/wiki/Decision_problem")
  p += ' that is of unprecedented simplicity and power.'
  d.p('''It is the alphabet of thought.''')

  d.p('''I'm still gathering threads and learning but I've compiled a few links and a bit of history:''')
  with d.ul as ul:
    ul.li('C. S. Pierce, Existential Graphs, circa 1890')
    ul.li('Spencer-Brown, "Laws of Form"')
    ul.li('Bricken, ').a('http://iconicmath.com/', href='http://iconicmath.com/')
    ul.li('Shroup, ').a('http://www.lawsofform.org/', href='http://www.lawsofform.org/')
    ul.li('Burnett-Stuart, ').a('http://www.markability.net/', href='http://www.markability.net/')
    ul.li('Kauffman, ').a('http://www.math.uic.edu/~kauffman', href='http://www.math.uic.edu/~kauffman')


def part_zero(d):
  d.h1('Nonsensical Formalities', align="center")

  d.p('''In the absence of all distinction nothing can be signified.''')
  d.p('''To make a distinction is to create the entire Universe, complete, Eternal, as it is now and ever shall be.  The "Word of God" is fractally encoded into the structure of structure at the most intrinsic and essential level.  Every tiniest least distinction made inherently contains or predicts or necessitates the entirety of everything you experience and have experienced and will experience, as well as the experiences of all other sentient beings everywhere throughout time.''')

  separator(d)

  d.p('''Observe an empty expanse.  For concreteness take the area below this sentence as a small space of the nondistinct Void.  (O Beloved Reader if you are without the visual sense the following can all be done in sound as well.)''')
  with d.blockquote as bl:
    bl.br ; bl.br ; bl.br
  d.p('''There, that was a little bit of the Void, without distinction.''')
  d.p('''Now consider this mark:''')
  d.blockquote.p('.')
  d.p('''That mark can be said to be "one thing", yes?''')
  d.p('''But a moment's reflection will let us understand there are three "things there":''')
  with d.ol as ol:
    ol.li('The inside of the mark.')
    ol.li('The outside of the mark.')
    ol.li('The distinction, the boundary, between inside and outside.')

  separator(d)

  d.p('''Having made any distinction the Universe is partitioned into two "spaces" and the boundary between them. We can naturally represent this situation with a closed figure such as a circle:''')
  d.blockquote.p(u'○')
  d.p(u'''But having done this to illustrate the triune nature of any distinction we can reflect again that this figure ○ has five parts: the inside and outside, the "inside" of the boundary, and the two boundaries separating the "inside" of the boundary from the outside-outside and the inside-outside.''')
  d.p('''This is a completely natural process.  Consider your location on the Earth.  The great majority of your life takes place on just such a boundary between the lava inward and the hard vacuum outward, and again on the boundary between the frozen-stone crust and the vaporous atmosphere.  If you stoop and examine conditions very close to this boundary you will discover additional boundaries to the limits of your perceptual apparatus.''')
  d.p('''This is a general phenomenon: the closer a sensory apparatus approaches in scale to a boundary, the more meta-boundaries it will resolve, up to its limits.''')

  separator(d)

  d.p('''Make a distinction,''')
  d.blockquote.p('.')
  d.p('''Notice that it partitions the Universe into the mark and the unmarked.''')
  d.blockquote.p(u'○')
  d.p('''We can imagine taking a perceptual position within the boundary itself and looking "outward" both to the distinct "inside-outside" and the "outside-outside" and perceiving "two things".  We can say that the Sky is around the Earth:''')
  d.blockquote.p(u'◎')
  d.p('''Or we can say that the Earth and the Sky are "two different things":''')
  d.blockquote.p(u'○○')
  d.p('''Either way, the boundary is the perceptual illusion that we name "the horizon".  A moment's reflection lets us understand that "the horizon" is not real except as "it" is perceived.  Continuing in this way, we discover that there "are" many "things" that only exist because we perceive and name them.  Continuing in this way, we discover that all "things" only exist because we perceive and name them.  If we neglect to distinguish and name "things" there is "no-thing" there.''')
  d.p('''A man named George Spencer-Brown developed a wonderful notation and wrote it in a book he called "Laws of Form".  That is where I first encountered it, from a reference in the Whole Earth Catalog.''')
  d.p('''If you are interested in the "mystical" aspects of this notation I urge you to read the Tao Te Ching (I recommend highly the translation by J. Star) and GSB's "Laws of Form".  The experiences of Dr. Jill Bolte Taylor are also of direct relevance.  A neuroanatomist who suffered a stroke, she was able to understand what was happening to her as the symbolic processing areas of her brain were impaired by the flooding blood.  During the time that her symbolic processing systems were mechanically disengaged, Dr. Taylor reports transcendent bliss and the non-ability to differentiate between "her" body and the "external" Universe of phenomenon.''')
  d.p('''No more will be said here about the transcendental function of the notation.''')


def part_one(d):
  d.h1('"Formal Nonsense"', align="center")

  d.p('''For our purposes it will suffice to understand the following rule:''')
  d.blockquote('A "mark" is a circle that is empty or contains no marks.')
  d.p('''You may find it worthwhile to play with some circles and use the rule to determine if the resulting forms count as "marks" or not.  For example these forms (taking paired parentheses to indicate closed circles) are "marks":''')
  d.blockquote((nbsp * 5).join((
    u'○',
    u'○○○',
    u'(◎)',
    u'○○',
    )))
  d.p('''While these forms are not "marks" (or "not-marks"):''')
  d.blockquote((nbsp * 5).join((
    u'◎',
    u'(○○)',
    u'(◎○)',
    u'((◎))',
    )))
  d.p('''Bricken has shown that two rules for "rewriting" or "transforming" these forms permit all possible forms to be generated or elucidated without altering the "mark"-ness of the resulting new forms.''')
  d.p('''These are the two rules (the Bricken basis):''')
  bl = d.blockquote(u'○ ↔ ○○') ; bl.br ; bl += u'nothing ↔ ◎'
  d.p('''These rules can be described in language in many ways. We can say that any mark is the same as any number of marks, and that the Void is the same as a non-mark.  Using the rules from left-to-right (in the above depiction) generates new forms, and using them right-to-left reduces forms back to either a mark or the Void.''')


def f(d):
  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')


def separator(n):
  n.div(u'◎', align="center")


if __name__ == '__main__':
  print index(blocks=(
    first,
    part_zero,
    part_one,
    ))
