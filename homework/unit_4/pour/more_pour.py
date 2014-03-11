
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []


## ORIGINAL POUR PROBLEM

def pour_problem(X, Y, goal, start=(0,0)):
    '''
    X and Y are the capacity of glasses; (x,y) is current fill levels 
    and represent a state. The goal is a level that can be in either 
    glass. Start at start state and follow successors until we reach 
    the goal. Keep track of frontier and previously explored; fail when 
    no frontier.
    
    '''
    if goal in start:
        return [start]
    explored = set() # set the states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        (x, y) = path[-1] # Last state in the first path of the frontier
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)

def solve(X, Y, goal, start=(0,0)):
    done = lambda state: goal in state
    next = lambda state: successors(*state, X=X, Y=Y)
    return shortest_path_search(start, next, done)

def successors(x, y, X, Y):
    '''
    Return a dict of {state:action} pairs describing what can be reached from
    the (x, y) state and how.
    
    '''
    assert x <= X and y <= Y ## (x, y) is glass levels; X and Y are glass sizes
    return {((0, y+x) if y+x <= Y else (x-(Y-y), y+(Y-y))): 'X->Y',
            ((x+y, 0) if x+y <= X else (x+(X-x), y-(X-x))): 'X<-Y',
            (X, y): 'fill X',
            (x, Y): 'fill Y',
            (0, y): 'empty X',
            (x, 0): 'empty Y'
            }

def test_pour():
    expected = [         (0, 0), 
            'fill Y',    (0, 9), 
            'X<-Y',      (4, 5), 
            'empty X',   (0, 5), 
            'X<-Y',      (4, 1), 
            'empty X',   (0, 1), 
            'X<-Y',      (1, 0), 
            'fill Y',    (1, 9), 
            'X<-Y',      (4, 6)]
    X, Y, goal = 4, 9, 6
    assert pour_problem(X, Y, goal) == solve(X, Y, goal) == expected

# test_pour()


## MORE POUR PROBLEM
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 

def more_successors(volumes, capacities):
    '''
    Return a dict of {state:action} pairs describing what can be 
    reached from given state of glass levels.
     
    '''
    next = {}
    for i, I in enumerate(capacities):
        state = set_i(volumes, i, I)
        next[state] = ('fill', i)
        state = set_i(volumes, i, 0)
        next[state] = ('empty', i)
        for j, J in enumerate(capacities):
            if i == j: continue
            state = pour(i, I, j, J, volumes)
            next[state] = ('pour', i, j)
    return next

def set_i(seq, i, value):
    s = list(seq)
    s[i] = value
    return type(seq)(s)

def pour(x, X, y, Y, volumes):
    '''Pour from x to y and return new tuple of volumes.'''
    state = list(volumes)
    total = state[x] + state[y] 
    if total <= Y:
        state[x] = 0
        state[y] = total
    else:
        diff = (Y - state[y])
        state[x] = state[x] - diff
        state[y] = state[y] + diff
    return tuple(state)

def more_pour_problem(capacities, goal, start=None):
    '''
    The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number.

    '''
    start = start or tuple(0 for c in capacities)
    done = lambda state: goal in state
    next = lambda state: more_successors(state, capacities)
    return shortest_path_search(start, next, done)
    
    
def test_more_pour():
    print more_pour_problem((1, 2, 4, 8), 4)
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]

    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
