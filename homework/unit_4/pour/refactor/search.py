from collections import namedtuple as named

def shortest_path(start, next, goal):
    """
    Find shortest path from start state to goal state.
    
    The next method should generate a list of possible 
    successor states from a given state.
    
    The goal method should test whether a given state is 
    a goal state or not.

    """
    if goal(start): return [start]
    seen = set()            # states already seen
    paths = [ [start] ]     # ordered list of paths taken
    while paths:
        path = paths.pop(0)
        last = path[-1]             # last state on path
        for state in next(last):    # successor states from last
            if state not in seen:
                seen.add(state)
                if goal(state):
                    return path+[state]
                else:
                    paths.append(path+[state])


if __name__ == '__main__':

    '''
    From a state, x, the only possible successors are x+1 and x-1. 
    Given a starting integer, find the shortest path to the integer 8.
    
    '''
    State = named('Integer', 'x, action')

    start = State(5, None)

    def goal(state): return state.x == 8
        
    def next(state): return [State(state.x+1, action='+'),
                             State(state.x-1, action='-')]

    expected = [State(5, None),
                State(6,'+'),
                State(7,'+'),
                State(8,'+')]

    assert shortest_path(start, next, goal) == expected

    start = State(10, None)
    expected = [State(10, None), 
                State(9,'-'), 
                State(8,'-')]
    assert shortest_path(start, next, goal) == expected
