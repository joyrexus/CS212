from collections import defaultdict
from boston import lines

def subway(**lines):
    """
    Define a subway map based on line names and each line's stations.

    Input args should be line name keywords with a string of stations as 
    values (e.g., red='alewife davis ...').

    Returns a dict of the form:
    { station: {neighbor: line, ... }, ...  }

    For example:
    dict(foresthills=dict(backbay='orange'), ... )

    """
    map = defaultdict(dict)
    for line, stations in lines.items():
        stations = dictify(stations)
        def neighbors(i):
            N = [stations.get(i-1, None), stations.get(i+1, None)]
            return (n for n in N if n)
        for i, station in stations.items():
            for n in neighbors(i):
                map[station][n] = line
    return map

def dictify(stations):
    '''Convert seq to enumerated dict form for easier index checking.'''
    return dict((i, name) for i, name in enumerate(stations.split()))

boston = subway(**lines)

def shortest_path_search(start, successors, is_goal):
    '''
    Find shortest path from start state to a state
    such that is_goal(state) is true.
    
    '''
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
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

def ride(here, there, system=boston):
    '''Return path on system from here to there.'''
    search = shortest_path_search
    next = lambda station: system[station]
    done = lambda station: station == there
    return search(here, next, done)

def longest_ride(system):
    '''Return longest possible ride between any two stops.'''
    rides = [ride(a, b) for a in system for b in system]
    return max(rides, key=len)

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


if __name__ == '__main__':
    expected = {
        'a': {'b': 'blue'}, 
        'x': {'c': 'blue', 'b': 'green'}, 
        'c': {'x': 'blue', 'b': 'blue', 'z': 'green'}, 
        'b': {'a': 'blue', 'x': 'green', 'c': 'blue', 'z': 'green'}, 
        'z': {'c': 'green', 'b': 'green'}
    }
    assert subway(blue='a b c x', green='x b z c') == expected

    assert boston['state'] == dict(downtown='orange', 
                                   haymarket='orange', 
                                   aquarium='blue', 
                                   government='blue')

    next = lambda station: boston[station]
    assert next('state') == boston['state']

    expected = ['mit', 'red', 'charles', 'red', 'park']
    assert ride('mit', 'park') == expected
