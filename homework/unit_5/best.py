import math

million = 1000000

def Q(state, action, U, verbose=False):
    '''Expected value of taking action in state according to utility U.'''
    Q.hold = lambda: U(state + 1 * million)
    Q.gamble = lambda: (U(state + 3 * million) + U(state)) * .5
    result = getattr(Q, action)
    if verbose:
        msg = 'Q(action={0}, state={1}, utility={2}") => {3}'
        print msg.format(action, state, U.__name__, result())
    return result()

def actions(state): return ['hold', 'gamble']   # note use of state arg!

def identity(x): return x

def best_action(state, actions, Q, U):
    '''Return optimal action for state, given utility U.'''
    EU = lambda action: Q(state, action, U)     # expected utility
    return max(actions, key=EU)

if __name__ == '__main__':

    actions = ['hold','gamble']
    assert best_action(100, actions, Q, identity) == 'gamble'
    assert best_action(100, actions, Q, math.log10) == 'hold'

    U = math.log10

    msg = 'Q({0}, {1}, {2}): {3}'
    for n in range(1, 5):
        state = n * million
        for action in actions:
            q =  Q(state, action, U)
            print msg.format(action, state, U.__name__, q)
            print

    state = 1 * million
    assert Q(state, 'gamble', U) == Q(state, 'hold', U)
