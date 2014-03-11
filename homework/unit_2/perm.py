from itertools import permutations, combinations

print 'Permutations of A, B C'
for i in permutations('ABC'):
    print i

print

print 'Combinations of A, B C, D chosen 3 at a time'
for i in combinations('ABCD', 3):
    print i

print

def permute(n=0):
    print 'Permutations of {0} digits'.format(n)
    for p in permutations(range(10), n):
        print p

# permute(2)
