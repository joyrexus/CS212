# write a function, bsuccessors2 that takes a state as input
# and returns a dictionary of {state:action} pairs.
# 
# The new representation for a path should be a list of 
# [state, (action, total time), state, ... , ], though this 
# function will just return {state:action} pairs and will
# ignore total time. 

def successors(state):
    '''
    Return a dict of {state:action} pairs. 
    
    A state is a (here, there) tuple, where here and there are 
    frozensets of people (indicated by their times) and/or the 'light'.

    Action is represented as a tuple (person1, person2, arrow), where 
    arrow is '->' for here to there and '<-' for there to here.
    
    '''
    here, there = state
    if 'light' in here:
        return dict((s, a) for s, a in move(here, there, '->'))
    else:
        return dict((s, a) for s, a in move(there, here, '<-'))

def move(origin, target, arrow):
    for a in origin:
        if a is 'light': continue
        for b in origin:
            if b is 'light': continue
            crossing = frozenset([a, b, 'light'])
            here, there = None, None
            if arrow == '->':
                here  = origin - crossing
                there = target | crossing
            else:
                there = origin - crossing
                here  = target | crossing
            state = (here, there)
            action = (a, b, arrow)
            yield state, action

def bsuccessors(state):
    """
    Return a dict of {state:action} pairs. 
    
    A state is a (here, there) tuple, where here and there 
    are frozensets of people (indicated by their travel times) 
    and/or the light.
    
    """
    here, there = state
    if 'light' in here:
        return dict(((here  - frozenset([a,b,'light']),
                      there | frozenset([a,b,'light'])),
                     (a, b, '->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here  | frozenset([a,b,'light']),
                      there - frozenset([a,b,'light'])),
                     (a, b, '<-'))
                    for a in there if a is not 'light'
                    for b in there if b is not 'light')  


def test():
    here, there = frozenset([1, 'light']), frozenset([])
    result = {(frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
    assert successors((here, there)) == result
    assert bsuccessors((here, there)) == result

    here, there = frozenset([1, 2, 'light']), frozenset([3])
    result = {
        (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'), 
        (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'), 
        (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')
        }
    assert successors((here, there)) == result
    assert bsuccessors((here, there)) == result


def bsuccessors3(state):
    """
    Return a dict of {state:action} pairs.  
    
	A state is a (here, there, light) tuple. Here and there are 
	frozensets of people (each person is represented by an integer
	which corresponds to their travel time), and light is 0 if 
	it is on the `here` side and 1 if it is on the `there` side.

	An action is a tuple of (travelers, arrow), where the arrow is
	'->' or '<-'. 

    """
    here, there, light = state
    if light == 0:
        return dict(((here  - frozenset([a,b]),
                      there | frozenset([a,b]), 1), (set([a,b]), '->'))
                        for a in here for b in here)
    else:
        return dict(((here  | frozenset([a,b]),
                      there - frozenset([a,b]), 0), (set([a,b]), '<-'))
                        for a in there for b in there)



def test_new():
    Z = frozenset

    result = bsuccessors3((Z([1]), Z([]), 0)) 
    expected = { (Z([]), Z([1]), 1)  :  (set([1]), '->') }
    assert result == expected

    assert bsuccessors3((Z([1, 2]), Z([]), 0)) == {
            (Z([1]), Z([2]), 1)    :  (set([2]), '->'), 
            (Z([]), Z([1, 2]), 1)  :  (set([1, 2]), '->'), 
            (Z([2]), Z([1]), 1)    :  (set([1]), '->')}

    assert bsuccessors3((Z([2, 4]), Z([3, 5]), 1)) == {
            (Z([2, 4, 5]), Z([3]), 0)   :  (set([5]), '<-'), 
            (Z([2, 3, 4, 5]), Z([]), 0) :  (set([3, 5]), '<-'), 
            (Z([2, 3, 4]), Z([5]), 0)   :  (set([3]), '<-')}
    return 'tests pass'

print test_new()
