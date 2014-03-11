from itertools import product
from fractions import Fraction

sex = 'BG'  # possible genders

def prod(*variables):
    return [''.join(p) for p in product(*variables)]

two_kids = prod(sex, sex)   # cartesian product (all possibilities)

at_least_one_boy = [s for s in two_kids if 'B' in s]

def two_boys(s):
    return s.count('B') == 2

def cond_prob(predicate, event):
    '''
    Conditional probability: P(predicate(s) | s in event).
    The proportion of states in event for which predicate is true.

    '''
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

print cond_prob(two_boys, at_least_one_boy)

'''
The above shows the condition probability of the predicate "your
mother will give birth to two boys" given the event of your mother having two
children, where at least one of the two is a boy.

Consider the event of having two children. There are four distinct
possibilities:

* boy, boy
* boy, girl
* girl, girl
* girl, boy

If we add the caveat "where at least one of the two is a boy", this restricts
the possibilites to three.

Of these three possibilities, the predicate is only true of one (viz., "boy,
boy").  Therefore, the conditional probability of the predicate given the
event is 1/3.


Now, consider the following problem:

Of all families with two children with at least one boy born on a Tuesday, what
is the probability of such a family having two boys?

'''

day = 'SMTWtFs'

two_kids_day = prod(sex, day, sex, day)

event = [k for k in two_kids_day if 'BT' in k]  # at least one boy born on Tues
pred = lambda e: e.count('B') == 2              # event contains two boys


print '''
Of all families with two children with at least one boy born on a Tuesday, what
is the probability of such a family having two boys?
'''
print cond_prob(pred, event)
# same as ...
print Fraction(sum(1 for e in event if pred(e)), len(event))
