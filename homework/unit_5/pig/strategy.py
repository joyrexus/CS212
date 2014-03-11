# Write a strategy function, clueless, that ignores the state and
# chooses at random from the possible moves (it should either 
# return 'roll' or 'hold'). Take a look at the random library for 
# helpful functions.

import random

possible_moves = ['roll', 'hold']

def clueless(state):
    'Strategy that ignores state and chooses at random from possible moves.'
    return random.choice(possible_moves) 


# In this problem, you will complete the code for the hold_at(x) 
# function. This function returns a strategy function (note that 
# hold_at is NOT the strategy function itself). The returned 
# strategy should hold if and only if pending >= x or if the 
# player has reached the goal.

def hold_at(x):
    '''
    Return a strategy that holds if and only if 
    pending >= x or player reaches goal.
    
    '''
    def strategy(state):
        (p, me, you, q) = state
        return 'hold' if (q+me >= goal or q >= x) else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

goal = 50

def test():
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10))  == 'roll'
    assert hold_at(15)((0, 2, 30, 15))  == 'hold'

test()
