# -*- coding: utf-8 -*-
from html import HTML


nbsp = u'\xa0'


def index(ht=None, blocks=()):

  if ht is None: ht = HTML()

  with ht.head as h:
    h.title('The Egg of Ouroboros Web Site')
    h.meta(charset='utf-8')
    h.link(
      href='http://fonts.googleapis.com/css?family=Inconsolata|EB+Garamond|Muli:400,300',
      rel='stylesheet',
      type_='text/css',
      )
    h.link(href='site.css', rel='stylesheet', type_='text/css')

  with ht.body as b:
    for block in blocks:
      d = b.div(class_="prose")
      block(d)
      b.hr
    copyright_notice(b)

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


def nomy(d):
  d.h3('In the Land of Nomy', align="center")

  bl = d.blockquote('Know names to find the Ten Thousand Things.')
  bl.br
  bl += 'No names am the Way'
  c = bl.cite
  c.br
  c += '~the Old Man'

  d.p('''Once we can generate myriad forms we can perform another trick that is somewhat mysterious and somewhat concrete (like the primal distinction.)  The name of this trick is "naming", and it is, in a sense, the opposite of Void.''')
  d.p('''The initial distinction can be considered a name for itself.  By existing (which it only does because you made it) the distinction distinguishes something from the Void, and as there is no other thing to name, it names itself.''')
  d.p('''The Void is unknowable, inexpressible, but every distinction is a self-creating "name".''')
  d.p('''Then we do something really special, we "let" one bit of the plenum over here "name" some other bit of the plenum over there.''')
  d.p('''One pattern of distinctions (which we can think about concretely using the circle language) can "stand for" another pattern. This is an arbitrary and meaningless thing to do, but once made such a linkage is more-or-less mechanical.''')
  d.p('''We can write dictionaries and train dogs to salivate at the sound of a certain bell.  (This later sort of naming is just at the inflection point between analog and digital computation, the dog "knows" a word but it could never give you a symbolic definition of it.  However, if you were somehow to "mention" the bell-sound in a way the dog could re-cognize, perhaps by beginning a motion identical to the motion you make to ring the bell but doing it in the absence of the actual bell, the dog would salivate.  Put another way, you can tell if the dog "thinks" you are "talking about" dinner-time by whether or not it salivates.)''')
  d.p('''Our own brains are constantly attempting to move pattern-handling from costly "thought" to cheaper pattern-recognition.  We are always coming up with "names" for new parts of the plenum as we understand their relevance and utility for "our lives".''')
  d.p('''Despite the occasional problems with this approach it has proven so useful (for certain kinds of "useful") that we have built machines to do it for us, faster and with greater range than our nervous systems can handle.  Computers are collections of "names" for automatic pattern manipulation, along with means for recombining the names to form new names to recognize and manipulate new patterns.''')
  d.p('''We call these names "programs" and the art and science of writing new names out of the old is called "computer programming".''')


def naming_0(d):
  d.p('''There are two ways of making names out of the circle language, and both are "cheating".''')
  d.p('''First, we can simply arrange patterns of circles to represent distinct symbols that we then "let stand for" other patterns.  This is how most kinds of printers actually work.  An "ink-jet" printer, for example, is precisely placing tiny circles of ink on the paper to make patterns that our nervous systems recognize.  A "dot-matrix" printer is just putting dots in a matrix.''')
  d.p('''The other way of naming patterns is to come up with some "ordering" convention for patterns, and then use those "numbers" to "index" any other sequence of patterns.''')
  d.p('''To make this concrete let's look at some possible orderings (let the underscore serve as an indicator of the Void.)  Here's one:''')
  blbr(d, (
    '_',
    u'○',
    u'○○',
    u'○○○',
    u'○○○○',
    ))
  d.p('''That's pretty simple. Here's another:''')
  blbr(d, (
    '_',
    u'○',
    u'◎',
    u'(◎)',
    u'((◎))',
    ))
  d.p('''Also pretty straightforward.  How about:''')
  blbr(d, (
    '_',
    u'○',
    u'◎',
    u'◎○',
    u'○◎',
    ))
  d.p('''But there's a problem with those last two patterns: they are actually the same pattern.  Circles "don't care" about the order of stuff. How could they when we haven't even finished figuring out what "order" even means yet?''')

  blbr(d, (
    '_',
    u'○',
    u'◎○',
    u'(◎○) ◎○',
    u'((◎○)◎○ ) (◎○)◎○',
    ))
  d.p('''It is a little difficult to see but the rule is anything gets replaced by a copy of itself inside a circle next to a copy of itself outside the circle.  This is a little unwieldy but it does generate patterns that don't repeat and are always unique.  But it's hardly the only way to go about it.''')
  d.p('''In a sense we are using these patterns as names for numbers, but in another sense numbers are just names for patterns that follow simple rules.  And, if we decided to "let" one of these sequences of patterns "stand for" an ordering, we are really just using the sequence as a kind of name aren't we?  But what are we naming with our sequence? Order?  But isn't the word "order" just a name for using a sequence as a name for "order"?  Where does this "order" really come from?''')


def naming_1(d):
  d.p('''For now, we will choose the first method in most of what follows and say that a letter, such as 'a', may be the name of some other pattern of circles.  "Just because."''')
  d.p('''(But really we know that the "letter" 'a' is just a bunch of little tiny circles jammed together in a squiggle with certain properties.  Later on we'll figure out how to talk about those properties properly but for now, "Just Because!")''')
  d.p('''But here's the really weird, the really bizarre and unreasonable thing we proceed to do next: we don't say what pattern of circles the name is a name for yet.''')
  d.p('''Now, whether you realize it or not, we're so used to doing this weird trick so automatically that we tend to forget just how mind-bendingly bizarre and unusual it is.''')
  d.p('''It's one thing to say a mark "names itself" because that's not really saying anything at all, at all, is it? If you say that the mark is saying itself, have you said anything?  And, if you weren't there saying that would the mark still be "a name"?  What kind of a question is that, anyway?''')
  d.p('''To say that a bit of pattern can "stand for" some other bit of pattern is, in comparison, quite reasonable.  "Smoke" means "fire" after all, doesn't it?''')
  d.p('''But when my friend says to me, "I have a friend, and I can't tell you his name, but..." don't I tend to know that there is a friend of my friend? But don't I tend to suspect that this friend's friend could be my friend, really? But maybe he is just making this up. After all, I'm just making him up.''')
  d.p('''So let's say that my friend's friend once told my friend, or so my friend informs me, that the squiggly line 'a' "is a name for" some pattern of circles, but I never found out which pattern of circles it was.''')
  d.p('''I know that every pattern of circles can reduce down to either the Void or a mark so I know this pattern "named" by 'a' must reduce down to one of those as well.''')
  d.p('''Consider this form:''')
  d.blockquote('(a(a))')
  d.p('''Even though I don't know what pattern of circles 'a' is a name for, I can still tell that this pattern of circles is Void-valued.  The easy way to think about a simple pattern like this one is to just imagine replacing 'a' wherever it appears with one of the two values (Void and Something Else) and then checking the result.''')
  d.p('''If 'a' is nothing at all then:''')
  d.blockquote.p(u'◎')
  d.p('''Which is Void-valued.  And if 'a' is a mark:''')
  d.blockquote.p(u'(○◎)')
  d.p('''Which is also Void-valued. So, no matter what 'a' might be (a(a)) is Void-valued.''')


def guardians_0(d):
  d.h3('The Guardians', align="center")
  d.p('''You have been captured by an evil wizard and imprisoned in a room.  There are two doors leading out of the room and in front of each door stands a mighty Guardian.  The wizard has informed you that one Guardian always tells the truth and the other Guardian always lies.  He has also informed you that one door leads to freedom while the other door leads to certain doom.  He didn't tell you which door is which, nor which Guardian is which, nor which door each Guardian is standing in front of, but he did tell you that you are allowed to ask one of the Guardians one question to figure out which door to go through..''')
  d.p('''What question should you ask?''')
  d.p('''If you know this riddle but don't remember the answer BEWARE! You may never forget it again after reading what's next.  This "riddle" will become so plain to your understanding that you will marvel that you ever thought it was a "riddle" in the first place.''')
  d.p('''Here we go...''')
  d.p(u'''Let us name the door that leads to freedom ◎ and the door that leads to certain doom ○, and let us name the Truth-Telling Guardian ◎ and the Lie-Telling Guardian ○.''')
  d.p(u'''If you were to ask the Truth-Teller what door he is standing in front of he will tell you the truth. If he is standing in front of the door leading to Freedom he would say ((◎)) (which is Void-valued) and if he is standing in front of the door leading to certain doom he would say (◎) (which is the same as ○).''')
  d.p(u'''The liar would say (◎) (which is the same as ○) if he is standing in front of the door leading to Freedom and ◎ (which is Void-valued) if he is standing in front of the door leading to certain doom.''')
  d.p('''That doesn't help much, but what if you asked one Guardian what the other Guardian would say if you were to ask him?''')
  d.p(u'''The Truth-Teller would tell the truth, so he would say the same thing that the Liar would say, but the liar would lie.  If the Truth-Teller is standing in front of the door leading to Freedom the liar would say that the Truth-Teller would say (((◎))) (which is the same as ○) but if the Truth-Teller is standing in front of the door leading to certain doom the liar would say ((◎)) (which is Void-valued.)''')
  d.p('''This is a little confusing so let's make a little table:''')
  with d.table(border='1') as t:
    with t.thead as th:
      th.td('Door')
      th.td('One Guardian')
      th.td('The Other Guardian')
      th.td('Answer')
    for row in (
      (u'○', u'○', u'◎', u'((◎)) -> Void'),
      (u'○', u'◎', u'○', u'((◎)) -> Void'),
      (u'◎', u'○', u'◎', u'(((◎))) -> ○'),
      (u'◎', u'◎', u'○', u'(((◎))) -> ○'),
      ):
      with t.tr as tr:
        for datum in row:
          tr.td(datum)
  d.p('''It seems that, no matter whom you ask, and no matter which door is which, you can find out the opposite of the answer you want by asking one Guardian what the other would say about his door.''')
  d.p('''In effect, by asking one Guardian what the other would say, you are forcing them both to answer, and because one always lies and one always tells the truth, and it doesn't matter in which order they go, you can always know the right answer, the door to Freedom.''')


def rules(d):
  d.p('''It turns out that if we follow two simple rules regarding names, in addition to the ones already described for plain circles, the resulting expressions can be made to enact something called the "Primary Logic".''')
  d.p('''The rules are simply:''')
  d.blockquote('"a name must stand for the same pattern wherever it is used in a circle-and-name expression"')
  d.p('''and''')
  d.blockquote(u'a(b) ↔ a(ab)')
  d.p('''And that's it.''')
  d.p('''If you follow those rules you can use the circle language to solve logic problems.''')


def guardians_1(d):
  d.h3('The Guardians Again', align="center")
  d.p('''Let's use 'd' for the "name" of a door and redraw our little diagram:''')

  with d.table(border='1') as t:
    with t.thead as th:
      th.td('Door')
      th.td('One Guardian')
      th.td('The Other Guardian')
      th.td('Answer')
    for row in (
      ('d', u'○', u'◎', '(((d))) -> (d)'),
      ('d', u'◎', u'○', '(((d))) -> (d)'),
      ):
      with t.tr as tr:
        for datum in row:
          tr.td(datum)
  d.p('''No matter which order the Guardians answer (Truth about a lie, or a lie about the Truth) if you can get them both in line they will always answer "(d)" and so tell you the name of the door.''')


def markable(d):
  d.p('''We can use circles and "names" to model and solve logical systems.''')
  d.p('''Many people, including George Spencer-Brown in "The Laws of Forms", have examined and explained this singular fact.  A man named George Burnett-Stuart has created a website "The Markable Mark" that provides a really wonderful and smooth introduction to the world of symbolic logic and formal reasoning using the notation of the Laws of Form, and it is his work which directly stimulated the paper you're reading now (any blame is mine, the inspiration is his.)''')
  d.p('''I really can't do better than Burnett-Stuart's "The Markable Mark".''')
  d.p('''I'm going to assume that you have gone and played your way through "The Markable Mark" to the point where you understand that any expression of circles and symbols "names" representing circle expressions, and symbols representing expressions of such symbols and circle expressions, and so on, can be manipulated in value-preserving ways by known logic.''')
  d.p('''Whenever a form can be reduced to either a mark or the Void for every possible set of values of the names in the form, the form is said to represent a "tautology".  Where this is not possible the form is said to represent a "satisfiable" statement, and the reduced form mentions each of the names that must be assigned values to be able to "satisfy" (or not) the statement.''')

  separator(d)

  d.p('''Names stand for logical terms and the concepts of logical statements can be expressed in the circle language according to the following (partial) translation table:''')
  d.p(u'''¬a     becomes        (a)''')
  d.p(u'''a ∧ b becomes  ((a)(b))''')
  d.p(u'''a ∨ b    becomes  ab''')
  d.p(u'''a → b    becomes  (a)b''')
  d.p(u'''a ← b  becomes   a(b)''')
  d.p(u'''a ↔ b   becomes  ((a(b))((a)b)) -or- ((a)(b))(ab)''')
  d.p(u'''a ↓ b  becomes   (ab)''')

  separator(d)

  d.p('''Some examples:''')
  d.p('''"All humans are mortal"''')
  d.blockquote('(mortal) human')
  d.p('''"John is mortal"''')
  d.blockquote('((John)(mortal))')
  d.p('''"John is human"''')
  d.blockquote('((John)(human))')
  d.p(u'''In order to determine if the first two statements support the third as a conclusion we perform the decision procedure:''')
  d.p(u'''Enclose the premises and concatinate with the conclusion (switching to single-letter names for ease of notation only):''')
  d.blockquote('((m)h) (((J)(m))) ((J)(h))')
  d.p(u'''Reduce.  We note that the middle term is wrapped and unwrap it:''')
  d.blockquote('((m)h) (J) (m) ((J)(h))')
  d.p(u'''We delete redundant subterms:''')
  d.blockquote('(h) (J) (m) ((h))')
  d.p(u'''Note that (h)((h)) matches a(a) if 'a' stands for '(h)' and therefore the expression is mark-valued, a tautology.  It would seem that John's mortality does indeed imply that he's human, although common sense dictates that we might need more information to be sure...''')
  d.p('''(Note that (h)((h)) becomes (h)h  by unwrapping, which is fine but not strictly necessary.  A machine solver might do it but we humans can let our brains figure out patterns any old which way they want to.)''')
  d.p('''The power and elegance of the notation are startling.''')
  d.p('''For example, logical statements that are equivalent under De Morgan's Laws are identical in the Circle Language.''')
  d.p('''If this were all then we have not said much that is not in any book on logic and symbolic reasoning.  If the only advantage to the Circle Language were that it gives a simple and elegant notation for formal reasoning then I would be satisfied, as that is a worthy and sorely needed thing.  Admirably, the notation also provides a means of constructing logical circuits and programs.''')
  d.p('''The resulting way of thinking about machines provides for a unified treatment of hardware and software, parallel and sequential operations, and self-acting (Cybernetic) systems.''')


def patterns(d):
  d.h3('Patterns', align="center")
  d.p('''(Index names from [Meguire 2007]):''')
  d.blockquote(u'C1. ((a)) = a')
  d.blockquote(u'C2. a(ab) = a(b)')
  d.blockquote(u'C3. ○a = ○')
  d.blockquote(u'C4. ((a)b)a = a')
  d.blockquote(u'C5. aa = a')
  d.blockquote(u'C6. ((a)(b))((a)b) = a')
  d.blockquote(u'C7. (((a)b)c) = (ac)((b)c)')
  d.blockquote(u'C8. ((a)(r))((b)r) = ((ab)(r))')
  d.blockquote(u'C9. (((a)(r))((b)r)) = (a(r))(br)')
  d.blockquote(u'J1. ((a)a) = ◎ = Void')
  d.blockquote(u'J2. ((ar)(br)) = ((a)(b))r')


def nor(d):
  d.h3('In the Land of Nor', align="center")
  d.p('''The key is to notice that a mark acts as a "NOR" gate on its contents.''')
  d.p('''A circle in the Circle Language "is":''')
  with d.ul as ul:
    ul.li('A signal')
    ul.li('The value of a signal')
    ul.li('An operation.')
  d.p('''A circle is both a value (term) and an action (name). This is a very subtle point and can be tricky to understand properly if you haven't encountered it before.  In the lambda calculus each lambda term is both a value and [the name for] an action to take on some values to derive or generate new values, which can themselves be lambda terms.  Likewise, in the SKI combinator calculus the combinators are both values and names of actions to take.  In computer programming, all programs are stored as sequences of bits, which are values.  The bits "name" the actions to take.''')
  d.p('''We can interpret the content-free Circle Language forms as networks of NOR (not-or) logic gates.  It is known art that all logic gate networks can be constructed out of NOR gates.  Therefore the Circle Language is a notation for digital logic circuits, and every digital logic circuit can be represented as a form of the Circle Language.''')
  d.p('''It is perhaps unnecessary to remark that all computers can be represented in the Circle Language.''')


def gm_0(d):
  d.p('''Each LoF mark form ("circle expression") is a specification of a network of logic gates and a proof of the expectable operation of that network. The proof proves the circuit and the circuit computes the proof.''')
  d.p('''Composing circle expressions composes the proofs and connects the circuits.''')
  d.p(u'''Two circle expressions that yield the same behaviour ("extensional identity") can have different properties otherwise (intentional dis-identity.)  This can be exploited to create programs and hardware with characteristics that are desirable while proving extensional identity with "correct" forms.  It should be possible to construct simple systems that search for extensionally identical forms of expressions automatically.  (cf. Gödel Machines.)''')


def circuits(d):
  d.h3('Circuits', align="center")
  d.p('''The circle language can be interpreted as digital logic circuits.''')
  d.blockquote(u'nor a, b -> (ab)')
  d.blockquote(u'or a, b -> ((ab))')
  d.blockquote(u'and a, b -> ((a)(b))')
  d.blockquote(u'nand a, b -> (((a)(b)))')
  d.blockquote(u'xor a, b -> (((a)(b))(ab))')
  d.p('''It should be understood that more than two symbols may appear within a form.  The symbols are taken to stand for any other pattern of circles, or circles and symbols, as described above in the section on using circle expressions to represent the formal logics, but here they also represent the "inputs" to the digital circuits.  The expressions themselves are the "outputs".''')
  d.p('''For concreteness we will develop a model of the Circle Language using the Python computer programming language.''')
  d.p('''In Python, let "a form" be any data-structure composed entirely of tuples.''')
  d.p('''The function "mark" reduces any form and returns True if the form is mark-valued and False if the form is Void-valued.  In Python it can be implemented as:''')
  d.code.pre('''\

    def mark(form):
      return not form or not any(mark(inner) for inner in form))

  ''')
  d.p('''This is a direct "translation" of the sentence. "A mark is circle that is empty or has no marks in it."  In Python the empty tuple is considered to have the Boolean value of False so we invert that value.  If the tuple/form has contents then we recursively examine them to determine if any of them are marks.  In effect we are performing a depth-first "walk" of a tree, and "short-circuiting" the walk as soon as we can determine the "mark"-ness of the tuple/form.''')
  d.p('''There are several improvements that could be made to this function, simple as it is.  We could "memoize" the function so that it did not re-compute the "mark"-ness of a form that it had "seen" before.  Also, it would be easy to manipulate our forms into a sort of standard form that ensured the "walk" terminated as early as possible.  For now we will neglect such considerations.''')


def f(d):
  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')

  d.p('''''')


def blbr(d, items):
  with d.blockquote(items[0]) as bl:
    for item in items[1:]:
      bl.br
      bl += item


def separator(n):
  n.div(u'◎', align="center")


def copyright_notice(b):
  d = b.div(class_="cp", align="center")
  a = d.a(rel="license", href="http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en_US")
  a.img(
    alt="Creative Commons License",
    style="border-width:0",
    src="http://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png")
  d.br
  d += '"'
  sp = d.span(
    'The Egg of Ouroboros',
    href="http://purl.org/dc/dcmitype/Text",
    property_="dct:title",
    rel="dct:type")
  sp.element.attrib['xmlns:dct'] = "http://purl.org/dc/terms/"

  d += '" by '

  sp = d.span('S.P. "Pedro" Forman', property_="cc:attributionName")
  sp.element.attrib['xmlns:cc'] = "http://creativecommons.org/ns#"
  d += ' is licensed under a '
  d.a(
    'Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License',
    rel="license",
    href="http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en_US",
    )
  d += '.'


def surreal(d):
  d.h3('Surreal Numbers', align="center")
  separator(d)
  d.p('''Conway was thinking about the game Go and found numbers. He told Knuth about them and Knuth went on vacation for a week and wrote a love story. Knuth said, "Call them Surreal Numbers." and Conway agreed, so that's what they're called.''')
  d.p('True story!')


if __name__ == '__main__':
  H = index(blocks=(
    first,
    part_zero,
    part_one,
    nomy,
    naming_0,
    surreal,
    naming_1,
    guardians_0,
    rules,
    guardians_1,
    markable,
    patterns,
    nor,
    gm_0,
    circuits,
    
    ))
  print H
  print >> open('index.html', 'w'), H
