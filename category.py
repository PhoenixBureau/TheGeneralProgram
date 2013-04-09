C = set((1, 2, 3))
hom = {}

for item in C:
  hom[item, item] = lambda n: n

f0 = lambda n: n + 1

hom[1, 2] = set()
hom[1, 2].add(f0)

hom[2, 3] = set()
hom[2, 3].add(f0)
 

machine = {
  '100': '110',
  '110': '010',
  '111': '000',
  '000': '110',
  '011': '001',
  }


def future(m, state, time):
  for _ in range(time):
    state = m.get(state, state)
  return state

