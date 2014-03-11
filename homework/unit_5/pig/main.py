# Write a function, max_diffs, that maximizes the point differential
# of a player. This function will often return the same action as 
# max_wins, but sometimes the strategies will differ.

from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    '''Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up.'''
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    _f.cache = cache
    return _f

other = {1:0, 0:1}

def roll(state, d):
    '''Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points.'''
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
    '''Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn.'''
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def Q_pig(state, action, Pwin):  
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)

def pig_actions(state):
    "The legal actions from a state."
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

goal = 40

@memo        
def Pwin(state):
    '''
    Return utility of current player winning from given state.

    Assumes opponent also plays with optimal strategy.

    '''
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin)
                   for action in pig_actions(state))

def Pwin2(state):
    'Return utility of current player winning from given state.'
    _, me, you, pending = state
    return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        state = (0, me, you, pending)
        return max(Q(state, action, Pwin2)
                   for action in pig_actions(state))

def Q(state, action, U):  
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - U(hold(state))
    if action == 'roll':
        return (1 - U(roll(state, 1))
                + sum(U(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError


@memo
def win_diff(state):
    "The utility of a state: here the winning differential (pos or neg)."
    (p, me, you, pending) = state
    if me + pending >= goal or you >= goal:
        return (me + pending - you)
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in pig_actions(state))

def max_diffs(state):
    '''
    A strategy that maximizes the expected difference between my 
    final score and my opponent's.
    
    '''
    return best_action(state, pig_actions, Q_pig, win_diff)

def max_wins(state):
    '''Use Pwin utility function to evaluate pig actions.'''
    return best_action(state, pig_actions, Q_pig, Pwin)


if __name__ == '__main__':

    def test():
        # The first three test cases are examples where max_wins and
        # max_diffs return the same action.
        assert(max_diffs((1, 26, 21, 15))) == "hold"
        assert(max_diffs((1, 23, 36, 7)))  == "roll"
        assert(max_diffs((0, 29, 4, 3)))   == "roll"
        # The remaining test cases are examples where max_wins and
        # max_diffs return different actions.
        assert(max_diffs((0, 36, 32, 5)))  == "roll"
        assert(max_diffs((1, 37, 16, 3)))  == "roll"
        assert(max_diffs((1, 33, 39, 7)))  == "roll"
        assert(max_diffs((0, 7, 9, 18)))   == "hold"
        assert(max_diffs((1, 0, 35, 35)))  == "hold"
        assert(max_diffs((0, 36, 7, 4)))   == "roll"
        assert(max_diffs((1, 5, 12, 21)))  == "hold"
        assert(max_diffs((0, 3, 13, 27)))  == "hold"
        assert(max_diffs((0, 0, 39, 37)))  == "hold"

        epsilon = 0.0001        # avoid floating point errors 
        assert goal == 40
        assert len(Pwin3.cache) <= 50000
        assert Pwin2((0, 42, 25, 0)) == 1
        assert Pwin2((1, 12, 43, 0)) == 0
        assert Pwin2((0, 34, 42, 1)) == 0
        assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
        assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon

    # test()

    import time

    def timedcall(fn, *args):
        "Call function with args; return the time in seconds and result."
        t0 = time.clock()
        result = fn(*args)
        t1 = time.clock()
        return t1-t0, result

    print 'Pwin:'
    print timedcall(Pwin, (0,0,0,0))
    print len(Pwin.cache)

    print 'Pwin2:'
    print timedcall(Pwin2, (0,0,0,0))
    print len(Pwin3.cache)
