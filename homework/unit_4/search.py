class Path(list):
    '''
    Representation of a path (sequence of states).

    '''
    def __init__(self, *args): super(Path, self).__init__(args)

    # make paths comparable by cost
    def __lt__(self, other): return self.cost < other.cost
    def __le__(self, other): return self.cost <= other.cost
    def __gt__(self, other): return self.cost > other.cost
    def __ge__(self, other): return self.cost >= other.cost
    def __add__(self, other): return Path(*list.__add__(self, other))

    @property
    def first(self):
        '''First element in path.'''
        return self[0]

    @property
    def last(self): 
        '''Last element in path.'''
        return self[-1]

    @property
    def cost(self):
        '''
        Cost of this path.
        
        The cumulative path cost should be specified in the 
        cost property of the last state in the path.

        '''
        return self.last.cost


class PathList(Path):
    '''
    List of paths, where each path is a sequence of states.

    '''
    def add(self, path):
        '''
        Add path, replacing costlier path (to same state) 
        if it exists.

        After adding, re-sort paths (by cost).

        '''
        for i, p in enumerate(self):
            if p.last == path.last:             # final states equivalent?
                if p.cost < path.cost:
                    return                      # existing path is better
                else:
                    del self[i]                 # existing path is worse
                    break
        super(PathList, self).append(path)      # add path
        self.sort()                             # re-sort paths by cost


def least_cost(start, next, goal):
    '''
    Return least cost path from start start state to goal state. 
    
    We begin with a start state, consider all successor states 
    of the last state on the best path (evaluated by cost) produced 
    by next(state), and conclude when goal(path) is true. 
    
    A path is a sequence of states and the cost of a path is the sum 
    of each state's action cost (state.action.cost).
    
    '''
    seen = set()                    # states already seen
    paths = PathList(Path(start))   # ordered list of paths taken
    while paths:
        path = paths.pop(0)         # remove first/best path
        if goal(path): 
            return path
        else:
            seen.add(path.last)     # add last to states seen
        for s in next(path.last):   # successors to last state
            if s not in seen:
                s.cost = s.action.cost + path.cost  # cost to get here
                paths.add(path+[s])                 # add extended path


def shortest(start, next, goal):
    """
    Find shortest path from start state to goal state.
    
    The next method should generate a list of possible 
    successor states from a given state.
    
    The goal method should test whether a given state is 
    a goal state or not.

    """
    seen = set()                        # states already seen
    if goal(start): return Path(start)
    paths = PathList(Path(start))       # ordered list of paths taken
    while paths:
        path = paths.pop(0)
        for state in next(path.last):   # successor states from last
            if state not in seen:
                seen.add(state)
                if goal(state):
                    return path+[state]
                else:
                    paths.append(path+[state])


if __name__ == '__main__':

    x = Path('a', 'b', 'c')
    y = Path('d', 'e', 'f')
    assert x.first is 'a'
    assert y.first is 'd'

    P = PathList(x, y)
    assert P.first is x
    assert P.last is y


    ## Example problem for shortest path search
    #
    # From a state, x, the only possible successors are x+1 and x-1. 
    # Given a starting integer, find the shortest path to the integer 8.
    from collections import namedtuple as named
    
    State = named('Integer', 'x, action')
    start = State(5, None)

    def goal(state): return state.x == 8
        
    def next(state): return [State(state.x+1, action='+'),
                             State(state.x-1, action='-')]

    expected = [State(5, None),
                State(6,'+'),
                State(7,'+'),
                State(8,'+')]
    assert shortest(start, next, goal) == expected

    start = State(10, None)
    expected = [State(10, None), 
                State(9,'-'), 
                State(8,'-')]
    assert shortest(start, next, goal) == expected
