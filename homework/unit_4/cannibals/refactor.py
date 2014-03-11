from paths import shortest
from collections import namedtuple as named


class EqualityMixin(object):
    '''
    A mixin class for checking equality among instances.
    
    '''
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class Action(EqualityMixin):
    '''
    Simple representation of an action that resulted in a new state.

    '''
    def __init__(self, missionaries, cannibals, direction):
        '''
        The constructor takes the number of missionaries moved, 
        cannibals moved, and the direction in which they were moved 
        to produce the resulting state.

        '''
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.direction = direction  # sent or returned

    def __repr__(self):
        msg = '{0} missionaries and {1} cannibals were {2}'
        return msg.format(self.missionaries, self.cannibals, self.direction)


# named tuples representing ...
Move = named('Move', 'missionaries, cannibals')     # number of each to move
Side = named('Side', 'missionaries, cannibals, boat')
State  = named('State', 'origin, target, action')


def next(state):
    '''Return list of next possible states from a given state.'''
    next = []
    moves = (Move(*t) for t in [(0,1), (1,0), (2,0), (1,1), (0,2)])
    origin, target, action = state
    assert origin.boat or target.boat and not (origin.boat and target.boat)
    if origin.cannibals > origin.missionaries > 0 or \
       target.cannibals > target.missionaries > 0: 
        return next
    if origin.boat:
        for move in moves:
            o = Side(*sub(origin, move), boat=False)
            t = Side(*add(target, move), boat=True)
            a = Action(*move, direction='sent')
            if all(x >= 0 for x in o+t):
                next.append(State(origin=o, target=t, action=a))
    else:
        for move in moves:
            o = Side(*add(origin, move), boat=True)
            t = Side(*sub(target, move), boat=False)
            a = Action(*move, direction='returned')
            if all(x >= 0 for x in o+t):
                next.append(State(origin=o, target=t, action=a))
    return next

def add(*vectors): return tuple(sum(t) for t in zip(*vectors))

def sub(*vectors): 
    return tuple(t[0] - sum(t[1:]) for t in zip(*vectors))

def inspect(X, Y):
    '''Inspect a list of states pairwise.'''
    for x, y in zip(X, Y):
        print x == y
        print x
        print y
        print

def test_next():
    origin = Side(missionaries=1, cannibals=4, boat=True)
    target = Side(missionaries=2, cannibals=2, boat=False)
    assert next(State(origin, target, None)) == [], "None possible"

    origin = Side(missionaries=2, cannibals=2, boat=True)
    target = Side(missionaries=0, cannibals=0, boat=False)
    state = State(origin, target, None)
    expected = [ 
        State(Side(2,1,False), Side(0,1,True), Action(0,1,'sent')),
        State(Side(1,2,False), Side(1,0,True), Action(1,0,'sent')),
        State(Side(0,2,False), Side(2,0,True), Action(2,0,'sent')),
        State(Side(1,1,False), Side(1,1,True), Action(1,1,'sent')),
        State(Side(2,0,False), Side(0,2,True), Action(0,2,'sent'))
    ]
    assert next(state) == expected

    origin = Side(missionaries=1, cannibals=1, boat=False)
    target = Side(missionaries=4, cannibals=3, boat=True)
    state = State(origin, target, None)
    expected = [ 
        State(Side(1,2,True), Side(4,2,False), Action(0,1,'returned')),
        State(Side(2,1,True), Side(3,3,False), Action(1,0,'returned')),
        State(Side(3,1,True), Side(2,3,False), Action(2,0,'returned')),
        State(Side(2,2,True), Side(3,2,False), Action(1,1,'returned')),
        State(Side(1,3,True), Side(4,1,False), Action(0,2,'returned'))
    ]
    assert next(state) == expected

test_next()


def solve(start, goal=None):
    '''
    Solve the missionaries and cannibals problem.  
    
    Find a path that goes from the initial state to goal.

    (If goal is not specified, it defaults to the the state with target 
    and origin reversed.)
    
    '''
    if goal is None:
        goal = State(start.target, start.origin, None)
    is_goal = lambda state: state.target == goal.target
    return shortest(start, next, is_goal)


def solve_orig(start, goal=None):
    '''
    Solve the missionaries and cannibals problem.  
    
    Find a path that goes from the initial state to goal.

    (If goal is not specified, it defaults to the the state with target 
    and origin reversed.)
    
    '''
    if goal is None:
        goal = State(start.target, start.origin, None)
    if start == goal:
        return [start]
    seen = set()            # states already seen
    paths = [ [start] ]     # ordered list of paths taken
    while paths:
        path = paths.pop(0)
        last = path[-1]
        for state in next(last):
            if state not in seen:
                seen.add(state)
                if state.target == goal.target:
                    return path+[state]
                else:
                    paths.append(path+[state])

def test_solve():
    origin = Side(missionaries=2, cannibals=1, boat=True)
    target = Side(missionaries=0, cannibals=0, boat=False)
    state = State(origin, target, None)
    expected = [ 
        State(Side(2,1,True), Side(0,0,False), None),
        State(Side(0,1,False), Side(2,0,True), Action(2,0,'sent')),
        State(Side(1,1,True), Side(1,0,False), Action(1,0,'returned')),
        State(Side(0,0,False), Side(2,1,True), Action(1,1,'sent'))
    ]
    assert solve(state) == expected
    assert solve_orig(state) == expected

    origin = Side(missionaries=1, cannibals=2, boat=True)
    target = Side(missionaries=0, cannibals=0, boat=False)
    state = State(origin, target, None)
    assert solve(state) == None
    assert solve_orig(state) == None

test_solve()
