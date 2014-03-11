import random
from collections import defaultdict

def shuffle1(p):
    n = len(p)
    swapped = [False]*n
    while not all(swapped):
        i, j = random.randrange(n), random.randrange(n)
        swap(p, i, j)
        swapped[i] = swapped[j] = True

def shuffle2(p):
    n = len(p)
    swapped = [False]*n
    while not all(swapped):
        i, j = random.randrange(n), random.randrange(n)
        swap(p, i, j)
        swapped[i] = True

def shuffle3(p):
    n = len(p)
    for i in range(n):
        swap(p, i, random.randrange(n))

def knuth(p):
    n = len(p)
    for i in range(n-1):
        swap(p, i, random.randrange(i, n))

def swap(p, i, j):
    p[i], p[j] = p[j], p[i]

def factorial(n):
    return 1 if n<= 1 else n * factorial(n-1)

def test_shuffle(shuffler, deck = 'abcd', n = 10000):
    counts = defaultdict(int)
    for _ in range(n):
        input = list(deck)
        shuffler(input)
        counts[''.join(input)] += 1
    e = n * 1./factorial(len(deck))
    ok = all((0.9 <= counts[item]/e <= 1.1) for item in counts)
    name = shuffler.__name__
    print '%s(%s) %s' % (name,  deck, ('ok' if ok else '*** BAD ***'))
    print '   ',
    for item, count in sorted(counts.items()):
        print "%s:%4.1f" % (item, count * 100. / n),
    print

def test_shufflers(shufflers = [knuth, shuffle1, shuffle2, shuffle3], 
                   decks = ['abc', 'ab']):
    for deck in decks:
        print
        for f in shufflers:
            test_shuffle(f, deck)

if __name__ == '__main__':
    test_shufflers()
