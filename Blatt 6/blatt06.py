# Aufgabe 1.2 - Square root

from math import sqrt
def sqrt_gen(start):
    current = start
    while True:
        yield sqrt(current)
        current += 1


# Aufgabe 1.3 - Permutations

def permute(input):
    letters = enumerate(input)
    if len(input) == 1:
        yield input
    else:
        for i, l in letters:
            if l not in input[:i]:  # check whether character was already used for permutations
                for j in permute(input[:i] + input[i + 1:]):
                    yield l + j
