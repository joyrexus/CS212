# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are 
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is 
# '->' for here to there or '<-' for there to here. When only one 
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.

def successors(state):
    '''
    Return a dict of {state:action} pairs. 
    
    A state is a (here, there) tuple, where here and there are 
    frozensets of people (indicated by their times) and/or the 'light'.

    Action is represented as a tuple (person1, person2, arrow), where 
    arrow is '->' for here to there and '<-' for there to here.
    
    '''
    here, there = state
    if 'light' in here:
        return dict((s, a) for s, a in move(here, there, '->'))
    else:
        return dict((s, a) for s, a in move(there, here, '<-'))

def move(origin, target, arrow):
    for a in origin:
        if a is 'light': continue
        for b in origin:
            if b is 'light': continue
            crossing = frozenset([a, b, 'light'])
            here, there = None, None
            if arrow == '->':
                here  = origin - crossing
                there = target | crossing
            else:
                there = origin - crossing
                here  = target | crossing
            state = (here, there)
            action = (a, b, arrow)
            yield state, action

def test_successors():
    here, there = frozenset([1, 'light']), frozenset([])
    result = {(frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
    assert successors((here, there)) == result

    here, there = frozenset([1, 2, 'light']), frozenset([3])
    result = {
        (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'), 
        (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'), 
        (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')
        }
    assert successors((here, there)) == result
    return 'Tests passed!'

# print test_successors()

def path_cost(path):
    """
    Total cost of path, stored in a tuple with the final action.
    
    path = [state, (action, total_cost), state, ... ]

    """
    if len(path) < 3: 
        return 0
    else:
        return path[-2][1]
        
def bridge_cost(action):
    """
    Return cost (a number) of an action in the bridge problem.

    An action is an (a, b, arrow) tuple; 
    a and b are times; arrow is a string. 

    """
    a, b, arrow = action
    return max(a, b)

def elapsed_time(path):
    return path[-1][2]

def bridge_problem(here):
    explored = set()                            # set of states visited
    here = frozenset(here) | frozenset(['light'])
    there = frozenset()
    state = (here, there)                       # initial state
    frontier = [[state]]                        # sorted list of paths blazed
    while frontier:
        path = frontier.pop(0)                  # get best path
        end_state = here, there = path[-1]          # get end state from path
        if not here or here == set(['light']):  # return if all have crossed
            return path
        explored.add(end_state)
        orig_cost = path_cost(path)
        for (state, action) in successors(end_state).items():
            if state not in explored:
                here, there = state
                cost = orig_cost + bridge_cost(action)
                new_path = path + [(action, cost), state]
                extend(frontier, new_path)
    return []

def final_state(path): return path[-1]

def extend(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    # (This could be done more efficiently.)
    # Find if there is an old path to the final state of this path.
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return # Old path was better; do nothing
    elif old is not None:
        del frontier[old] # Old path was worse; delete it
    ## Now add the new path and re-sort
    frontier.append(path)
    frontier.sort(key=path_cost)


if __name__ == '__main__':

    def test():
        path = bridge_problem(frozenset((1, 2),))
        assert path_cost(path) == 2 

        path = bridge_problem(frozenset((1, 2, 5, 10),)) 
        assert path_cost(path) == 17

        return 'Tests passed!'

    print test()
