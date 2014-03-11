
'''
Write a function, play_pig, that takes two strategy functions as input,
plays a game of pig between the two strategies, and returns the winning
strategy.

States are represented as a tuple of (p, me, you, pending) where
p:       an int, 0 or 1, indicating which player's turn it is.
me:      an int, the player-to-move's current score
you:     an int, the other player's current score.
pending: an int, the number of points accumulated on current turn, not yet
scored

'''

import random

other = {1:0, 0:1}
goal = 50

def hold(state):
    """
    Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn.
    
    """
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def roll(state, d):
    """
    Apply the roll action to a state (and a die roll d) to yield 
    a new state.
    
    """
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

dice = iter(lambda: random.randint(1,6), 0)

def play_pig(A, B, dice=dice):
    """
    Play a game of pig between two players, represented by their 
    strategies.

    Each time through the main loop we ask the current player for 
    one decision, which must be 'hold' or 'roll', and we update the 
    state accordingly.

    When one player's score exceeds the goal, return that player.
    
    """
    state = (0, 0, 0, 0)    # initial state
    player = (A, B)
    while True:
        (p, me, you, pending) = state
        if me >= goal:
            return player[p]
        elif you >= goal:
            return player[other[p]]
        decision = player[p](state)     # get decision for player p
        if decision is 'roll':
            state = roll(state, next(dice))
        else:
            state = hold(state)


# strategies

def clueless(state): return random.choice(['roll', 'hold'])

def always_roll(state): return 'roll'

def always_hold(state): return 'hold'

def hold_at(x):
    'Return strategy that holds iff pending >= x or score >= goal.'
    def strategy(state):
        (p, me, you, pending) = state
        return 'hold' if (pending >= x or me + pending >= goal) else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy


def test():
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'

    A, B = hold_at(50), clueless
    dice = iter(lambda: 6, 0)
    assert play_pig(A, B, dice) == A

test()
