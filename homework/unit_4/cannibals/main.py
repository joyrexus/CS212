def csuccessors(state):
    """
    Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.
    
    """
    M1, C1, B1, M2, C2, B2 = state
    assert B1 is 1 or B2 is 1
    pairs = {} 
    moves = [(0,1), (1,0), (1,1), (2,0), (0,2)]
    if C1 > M1 or C2 > M2: 
        return pairs         # more cannibals than missionaries
    if B1 is 1:
        B1, B2 = 0, 1
        for m, c in moves:
            if M1 - m >= 0 and C1 - c >= 0:
                state = (M1-m, C1-c, B1, M2+m, C2+c, B2)
                action = 'M' * m + 'C' * c + '->'
                pairs[state] = action
    else:
        B1, B2 = 1, 0
        for m, c in moves:
            if M2 - m >= 0 and C2 - c >= 0:
                state = (M1+m, C1+c, B1, M2-m, C2-c, B2)
                action = '<-' + 'M' * m + 'C' * c
                pairs[state] = action
    return pairs


def solve(start=(3,3,1,0,0,0), goal=None):
    """
    Solve the missionaries and cannibals problem.  
    
    State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) 
    sides.  Find a path that goes from the initial state to the goal state 
    (which, if not specified, is the state with no people or boats on the 
    start side.)
    
    """
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    if start == goal:
        return [start]
    explored = set()        # explored states
    frontier = [ [start] ]  # ordered list of paths taken
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)


def test(verbose=False):
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',  \
                                               (1, 2, 0, 1, 0, 1): 'M->',  \
                                               (0, 2, 0, 2, 0, 1): 'MM->', \
                                               (1, 1, 0, 1, 1, 1): 'MC->', \
                                               (2, 0, 0, 0, 2, 1): 'CC->'}

    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',  \
                                               (2, 1, 1, 3, 3, 0): '<-M',  \
                                               (3, 1, 1, 2, 3, 0): '<-MM', \
                                               (1, 3, 1, 4, 1, 0): '<-CC', \
                                               (2, 2, 1, 3, 2, 0): '<-MC'}

    assert solve((1,0,1,0,0,0)) == [(1,0,1,0,0,0), 'M->', (0,0,0,1,0,1)]
    assert solve((1,1,1,0,0,0)) == [(1,1,1,0,0,0), 'MC->', (0,0,0,1,1,1)]
    assert solve((2,1,1,0,0,0)) == [(2,1,1,0,0,0), 'MC->',
                                    (1,0,0,1,1,1), '<-C',
                                    (1,1,1,1,0,0), 'MC->',
                                    (0,0,0,2,1,1)]
    assert solve((1,2,1,0,0,0)) == None
    if verbose: print 'OK'

test()
