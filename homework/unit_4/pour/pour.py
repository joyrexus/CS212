import doctest

'''
Pouring actions:

    1. X to Y
    2. Y to X
    3. X to Z
    4. Y to Z
    5. Z to X
    6. Z to Y

'''

def pour_problem(X, Y, goal, start = (0, 0)):
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
    return Fail
Fail = []

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

class Test:
    '''
    >>> successors(0, 0, 4, 9)
    {(0, 9): 'fill Y', (0, 0): 'empty Y', (4, 0): 'fill X'}

    >>> successors(3, 5, 4, 9)
    {(4, 5): 'fill X', (4, 4): 'X<-Y', (3, 0): 'empty Y', (3, 9): 'fill Y', (0, 5): 'empty X', (0, 8): 'X->Y'}

    >>> successors(3, 7, 4, 9)
    {(4, 7): 'fill X', (4, 6): 'X<-Y', (3, 0): 'empty Y', (0, 7): 'empty X', (3, 9): 'fill Y', (1, 9): 'X->Y'}

    >>> pour_problem(4, 9, 6)
    [(0, 0), 'fill Y', (0, 9), 'X<-Y', (4, 5), 'empty X', (0, 5), 'X<-Y', (4, 1), 'empty X', (0, 1), 'X<-Y', (1, 0), 'fill Y', (1, 9), 'X<-Y', (4, 6)]

    '''

print doctest.testmod()     # TestResults(failed=0, attempted=9)


## What problem, with X, Y, and goal < 10 has the longest solution?
## Answer: pour_problem(7, 9, 8) with 14 steps.

def num_actions(triple):
    X, Y, goal = triple
    return len(pour_problem(X, Y, goal)) / 2

def hardness(triple):
    X, Y, goal = triple
    return num_actions(triple) - max(X, Y)

A = max([(X, Y, goal) for X in range(1, 10) 
                      for Y in range(1, 10)
                      for goal in range(1, max(X, Y))], key = num_actions)

B = max([(X, Y, goal) for X in range(1, 10) 
                      for Y in range(1, 10)
                      for goal in range(1, max(X, Y))], key = hardness)
assert A == B == (7, 9, 8)

expected = [(0, 0), 'fill Y', 
            (0, 9), 'X<-Y', 
            (7, 2), 'empty X', 
            (0, 2), 'X<-Y', 
            (2, 0), 'fill Y', 
            (2, 9), 'X<-Y', 
            (7, 4), 'empty X', 
            (0, 4), 'X<-Y', 
            (4, 0), 'fill Y', 
            (4, 9), 'X<-Y', 
            (7, 6), 'empty X', 
            (0, 6), 'X<-Y', 
            (6, 0), 'fill Y', 
            (6, 9), 'X<-Y', 
            (7, 8)]

assert pour_problem(X=7, Y=9, goal=8) == expected

