  N = lambda bits: sum(2**n for n, bit in enumerate(reversed(bits)) if bool(bit))
