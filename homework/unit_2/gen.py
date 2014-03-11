from util.profile import Counter

count = Counter('Iterations through *neg_every_other_int*')

def ints(start=1, end=None):
    i = start
    while i <= end or end is None:
        yield i
        i = i + 1
    
def signed_ints():
    '''Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ... '''
    yield 0
    for i in ints():
        yield +i
        yield -i

def neg_every_other_int(*args):
    '''Negate every other integer.'''
    sign = 1
    for i in count(ints(*args)):
        yield sign * i
        sign *= -1

# for i in count(range(10)): pass

for i in neg_every_other_int(1, 10): pass 
for i in neg_every_other_int(1, 5): pass

print count
