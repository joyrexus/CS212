from search import Path, PathList
from search import least_cost as search


class Side(frozenset):
    '''
    Representation of one side of bridge, comprised of a set of 
    integers (representing individual people and the time it takes 
    them to cross the bridge) and optionally the string '*' 
    (representing the flashlight needed when crossing).

    '''
    def __new__(cls, *args):
        return frozenset.__new__(cls, args)


class Action:
    '''
    Representation of a crossing action resulting in a new state
    of the bridge problem.

    '''
    def __init__(self, *crossing):
        '''
        The args should be integers indicating who is crossing.

        '''
        self.crossing = set(crossing)
        self.cost = max(crossing) if crossing else 0

    def __repr__(self):
        attrs = ('cost', 'crossing')
        args = ['{0}={1}'.format(x, getattr(self, x)) for x in attrs]
        return 'Action({0})'.format(', '.join(args))


class State:
    '''
    Representation of a state of the bridge problem.
    
    A state has the following attributes:
    * left (frozenset): people on left side of bridge
    * right (frozenset): people on right side of bridge
    * light (string): "L" or "R" to indicate side that light is on
    * action (tuple): action resulting in current state
    * cost (int): total cost to reach current state

    The left/right attributes should be sets (frozensets) of
    people indicated by integers and/or the string "*" 
    (representing the flashlight needed to cross).

    '''
    def __init__(self, left=tuple(), 
                       right=tuple(), light="L", action=tuple(), cost=0): 
        self.left = Side(*left)
        self.right = Side(*right)
        self.light = light                    # side that light is on
        self.action = Action(*action)         # action producing current state
        self.cost = cost or self.action.cost  # cost to reach current state

    def __eq__(self, other):
        if self.left == other.left and \
           self.right == other.right and \
           self.light == other.light:
            return True

    def __hash__(self):
        '''Make states hashable based on left/right/light status.'''
        return hash((self.left, self.right, self.light))

    def __repr__(self):
        attrs = ('left', 'right', 'light', 'action', 'cost')
        args = ['{0}={1}'.format(x, getattr(self, x)) for x in attrs]
        return 'State({0})'.format(', '.join(args))


def next(state):
    '''
    Return next possible states from given state.
    
    A state has the following attributes:
    * left (frozenset/Side): people on left side of bridge
    * right (frozenset/Side): people on right side of bridge
    * light (string): side of bridge that flashlight is on
    * action (tuple/Action): action resulting in current state
    * cost (int): total cost to reach current state
    
    '''
    if state.light is "L":
        return set(State(state.left  - set([a,b]),
                         state.right | set([a,b]), light='R', action=(a,b))
                            for a in state.left for b in state.left)
    else:
        return set(State(state.left  | set([a,b]),
                         state.right - set([a,b]), light='L', action=(a,b))
                            for a in state.right for b in state.right)



def solve(*start):
    '''
    Solve the bridge problem.

    Find the fastest (least elapsed time) path to the goal, which
    is to get everyone across. That is, we want to get every person 
    on left side to right side in the least amount of time.  
    
    We can check to see that we've reached the goal state by checking 
    that the left side of the last state in the path (path.last.left) 
    is empty. (If the left side of the final state is empty, everyone 
    has crossed.)

    '''
    start = State(start)
    done = lambda path: not path.last.left  # left side of end state empty?
    return search(start, next, done)
    

if __name__ == '__main__':
    Z = frozenset

    L = Side(1, 4, 5)
    R = Side()
    assert L == Z([1,4,5]) == Side(1, 4, 5)
    assert R == Z([])

    state = State(L)
    assert state == State(left=(1,4,5), cost=0)
    assert state.right == Z([]) == Side()
    assert not state.right
    assert state.left

    expected = [
        State(left=[1]),
        State(right=[1], light="R", action=[1], cost=1)
    ]
    assert solve(1) == expected

    expected = [
        State(left=[1,2]),
        State(right=[1,2], light="R", action=(1,2), cost=2)
        ]
    assert solve(1, 2) == expected
