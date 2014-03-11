from collections import namedtuple as named

def shortest(start, next, goal):
    """
    Find shortest path from start state to goal state.
    
    next should generate a list of possible successor states
    from a given state; goal should test whether a given
    state is a goal state or not.

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


def test_example():
    '''
    From a state, x, the only possible successors are x+1 and x-1. 
    Given a starting integer, find the shortest path to the integer 8.
    
    '''
    State = named('Integer', 'x, action')

    start = State(5, None)

    def goal(state): return state.x == 8
        
    def next(state): return [State(state.x+1, action='next'),
                             State(state.x-1, action='prev')]

    expected = [State(5, None),
                State(6,'next'),
                State(7,'next'),
                State(8,'next')]

    assert shortest(start, next, goal) == expected

    start = State(10, None)
    expected = [State(10, None), State(9,'prev'), State(8,'prev')]
    assert shortest(start, next, goal) == expected

if __name__ == '__main__':

    test_example()
