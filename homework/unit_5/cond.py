import itertools
from fractions import Fraction

def product(*variables):
    'The cartesian product (as a str) of the possibilities for each variable.'
    return map(''.join, itertools.product(*variables))

def condP(predicate, event):
    '''
    Return the conditional probability of predicate given event:
        
        P(predicate(s) | s in event)

    This is just the proportion of states in event for which predicate is true.

    '''
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

def report(predicate, predname, cases, verbose=False):
    import textwrap
    for (name, event) in cases:
        print('P(%s | %s) = %s' % (predname, name, condP(predicate, event)))
        if verbose:
            print('Reason:\n"%s" has %d elements:\n%s' %(
                name, len(event), textwrap.fill(' '.join(event), 85)))
            good = [s for s in event if predicate(s)]
            print('of those, %d are %s:\n%s\n\n' % (
                len(good), predname, textwrap.fill(' '.join(good), 85)))

if __name__ == '__main__':

    sex = 'BG'
    two_kids = product(sex, sex)
    one_boy = [s for s in two_kids if 'B' in s]
    two_boys = lambda s: s.count('B') == 2          # state contains two boys

    # Out of all families with two kids with at least one boy 
    # what is the probability of two boys?
    assert condP(two_boys, one_boy) == Fraction(1, 3)

    day = 'SMTWtFs'
    two_kids_bday = product(sex, day, sex, day)
    boy_tuesday = [s for s in two_kids_bday if 'BT' in s]

    # Out of all families with two kids with at least one boy born on a
    # Tuesday, what is the probability of two boys?
    assert condP(two_boys, boy_tuesday) == Fraction(13, 27)

    boy_anyday = [s for s in two_kids_bday if 'B' in s]
    month = 'JFMAmjLaSOND'
    two_kids_bmonth = product(sex, month, sex, month)
    boy_december = [s for s in two_kids_bmonth if 'BD' in s]

    cases = [('2 kids', two_kids), 
             ('2 kids born any day', two_kids_bday),
             ('at least 1 boy', one_boy),
             ('at least 1 boy born any day', boy_anyday),
             ('at least 1 boy born on Tuesday', boy_tuesday),
             ('at least 1 boy born in December', boy_december)]

    report(predicate=two_boys, predname='2 boys', cases=cases, verbose=False)
    '''
    P(2 boys | 2 kids) = 1/4
    P(2 boys | 2 kids born any day) = 1/4
    P(2 boys | at least 1 boy) = 1/3
    P(2 boys | at least 1 boy born any day) = 1/3
    P(2 boys | at least 1 boy born on Tuesday) = 13/27
    P(2 boys | at least 1 boy born in December) = 23/47
    '''

    # report(verbose=True)
    '''
    P(2 boys | 2 kids) = 1/4
    Reason: "2 kids" has 4 elements (BB BG GB GG) and of those, 1 are 2 boys (BB)

    P(2 boys | 2 kids born any day) = 1/4
    Reason: "2 kids born any day" has 196 elements and of those, 49 are 2 boys

    P(2 boys | at least 1 boy) = 1/3
    Reason: "at least 1 boy" has 3 elements (BB BG GB) 
            and of those, 1 are 2 boys (BB)

    P(2 boys | at least 1 boy born any day) = 1/3
    Reason: "at least 1 boy born any day" has 147 elements 
            and of those, 49 are 2 boys

    P(2 boys | at least 1 boy born on Tuesday) = 13/27
    Reason: "at least 1 boy born on Tuesday" has 27 elements 
            and of those, 13 are 2 boys

    P(2 boys | at least 1 boy born in December) = 23/47
    Reason: "at least 1 boy born in December" has 47 elements
            and of those, 23 are 2 boys
    '''
