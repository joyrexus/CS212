from collections import namedtuple as named
from itertools import chain


def spots(start, n, inc=1):
    '''
    Return a tuple of `n` spots (indices on the grid), 
    starting at `start` and incrementing by `inc`.
    
    '''
    return tuple(start + (inc * i) for i in range(n))

def wall(n, as_set=False):
    '''Return indices of wall.'''
    upper = spots(0, n)
    left = spots(0, n, n)
    right = spots(n-1, n, n)
    lower = spots(n * (n-1), n)
    indices = set(upper + left + right + lower) - set(goal(n))
    return indices if as_set else tuple(indices)

def goal(n):
    'Return tuple containing index of goal (middle of RH-side of n x n grid).'
    i = None
    if n % 2:
        x = (n * n / 2)         # find middle index of middle row
        i = row(x,n)[-1]        # get last element of row with x
    else:
        i = (n * n / 2) - 1     # find middle indice directly
    return tuple([i])

def grid(cars, n):
    '''
    Return a tuple of (object, locations) pairs -- the expected format.

    The grid to be returned represents a state of the parking lot.  It's
    comprised of the following objects: a wall, a goal, and a number of cars.   

    The wall consists of the indices along the perimeter of the n x n grid.

    The goal is always located in the middle of the right-hand wall.

    The `cars` arg should be a tuple of (car, spots) pairs.  So, we're 
    basically adding two additional pairs for the wall and goal spot.

    That is, we're adding in info about the parking lot perimeter 
    (N x N) and goal spot to the info already given about the cars.
    
    '''
    return cars + (('@', goal(n)), ('|', wall(n)))
    
def show(state, n, action=None):
    '''Print out state of parking lot as n x n grid.'''
    if action:
        desc = "After offsetting {0} by {1}:".format(*action)
        print
        print desc
    grid = ['.'] * n**2                 # init and fill grid
    for (x, spots) in state:
        for s in spots:
            grid[s] = x
    for i, spot in enumerate(grid):     # print spots on grid
        print spot,
        if i % n == n - 1: print

Car = named('Car', 'size, unit, spaces')

is_car = lambda x: x not in ("@", "|")  # ignore wall and goal space

def inventory(state, n):
    '''
    Return a dict-based inventory of car specs in state.

    The dict of specs uses car names as keys, with Cars 
    (named tuples) as values.

    A Car is a named tuple with the attributes:
    size - a car's size (number of spots it uses)
    unit - row/column of spaces in which car sits
    spaces - spots in unit car can be moved to if
             not already occupied

    '''
    return dict((car, Car(len(spots), unit(spots,n), spaces(spots,n)))
                for car, spots in state if is_car(car))

def unit(spots, n):
    '''
    Return the unit (row or column) of spaces in which the car
    occupying spots (on n x n grid) resides.

    '''
    orient = orientation(spots)     # vertical or horizontal?
    i = spots[0]                    # lead spot/index/position
    spaces = column(i,n) if orient is "v" else row(i,n)
    spaces = sorted(tuple(set(spaces) - wall(n, as_set=True))) # omit wall spots
    return set(spaces)

def spaces(spots, n):
    '''
    Return tuple of spaces (empty spots) that the car currently
    occupying spots (indices indicating its current positon 
    on grid) can move if not already occupied.

    '''
    extra = len(spots) - 1              # extra spots taken up by car's length
    u = sorted(list(unit(spots, n)))    # spaces for car's row/column
    return set(u[:-extra])              # omit extra part from spaces 

def row(i, n):
    '''Return indices of row containing index i in n x n grid.'''
    return spots((i / n) * n, n)

def column(i, n):
    '''Return indices of column containing index i in n x n grid.'''
    return spots(i % n, n, n)

def orientation(spots):
    '''Return orientation (v|h) of car given the spots it occupies.'''
    return "h" if spots[1] - spots[0] == 1 else "v"

def done(state):
    '''
    Tests whether the location of our car contains the index 
    of the goal space.

    State should be a dict containing (car, spots) pairs.

    '''
    s = dict(state)
    goal = s['@'][0]
    return goal in s['*']

def step(state, specs):
    '''
    Yields a successor state (and action) from given state.

    States should be pairs of parking lot object labels
    and a tuple of the spots they occupy (indices on the 
    parking lot grid).

    Actions are represented as (car, offset) pairs where the 
    offset indicates how much the starting spot (an integer 
    index on the grid) of car was offset to move it to the 
    new spot.
    
    '''
    for car, spots in state:
        if not is_car(car): continue    # ignore wall and goal space
        for offset in moves(car, spots, state, specs):
            yield move(car, offset, state)

def moves(car, spots, state, specs, verbose=False):
    '''
    Yield valid moves for car in state.
    
    A move is an integer indicating how much to offset
    the leading index of the car.

    A car's spots are the indices on the parking lot
    grid it currently occupies.

    We use our pre-set inventory of car specs to check
    for potential spaces in which the car can move and 
    then make sure those spaces are not occupied by other 
    cars.  These are the empty spots the car might be 
    moved to if accessible (i.e., there are no spots 
    taken between car's current position and empty spot).

    '''
    i = spots[0]                                # car's current spot
    extra = set(spots[1:])                      # extra spots taken up by car
    unit = specs[car].unit                      # car's row/column of spaces
    spaces = specs[car].spaces                  # of which some are moveable to
    taken = (occupied(state) & unit) - set(spots) # taken spots in row/column
    empty = spaces - taken                      # empty spots in row/column
    if verbose:
        print 'Spots occupied by car:', spots
        print 'Extra spots of car:', extra
        print "The car's unit of spaces (row/col):", unit
        print 'Potential spaces for car in unit:', spaces
        print 'Taken spaces in unit:', taken
        print 'Empty spaces in unit:', empty
        print
    for e in empty:
        # check that spots taken between current and empty
        if any(i > t > e for t in taken): continue
        if any(i < t < e for t in taken): continue
        offset = e - i      
        # check that offset of extra spots is not taken
        if any(x + offset in taken for x in extra): continue
        # then yield any offset value other than zero
        if offset != 0: yield offset

def move(car, offset, state):
    '''
    Return successor state and action resulting in new state.

    The new state is just the current state but car moved.
    That is, we offset the leading index of car in the given 
    state to produce the new state.

    The action is just the pair (car, offset).

    '''
    s = dict(state)
    s[car] = tuple(i + offset for i in s[car])
    action = (car, offset)
    return (tuple(s.items()), action)

def occupied(state):
    '''Return set of occupied spots in state.'''
    taken = [spots for x, spots in state if is_car(x)]
    return set(chain(*taken))

def shortest(start, step, done, verbose=False):
    '''
    Find shortest path from start state to goal state.
    
    The step method should generate a list of possible 
    successor states from a given state.
    
    The done method should test whether a given state is 
    a goal state or not.

    '''
    if done(start): return [start]
    seen = set()            # states already seen
    paths = [ [start] ]     # ordered list of paths taken
    while paths:
        path = paths.pop(0)
        last = path[-1]                     # last state on path
        for state, action in step(last):    # successor states from last
            if state not in seen:   
                seen.add(state)
                P = path + [action, state]
                if done(state):
                    return P
                else:
                    paths.append(P)

def solve(start, n, verbose=False):
    '''
    Return solution path for parking puzzle described by `start`,
    where `n` is an integer indicating an n x n grid size.
    
    '''
    I = inventory(start, n)                         # do inventory once
    def next(state): return step(state, specs=I)    # and pass it in
    path = shortest(start, next, done)
    if verbose:
        for state, action in zip(states(path), actions(path)):
            show(state, n)
            print 
            print "After offsetting {0} by {1}:".format(*action)
        final = path[-1]
        show(final, n)
    return path

def solve_parking_puzzle(start, N=8): return solve(start, N)

def actions(path):
    '''Return a list of actions in this path.'''
    return path[1::2]

def states(path):
    '''Return a list of states in this path.'''
    return path[::2]


if __name__ == '__main__':
    #  start state ...
    # | | | | | | | |     |  |  |  |  |  |  |  |
    # | G G . . . Y |     |  9 10 11 12 13 14  |
    # | P . . B . Y |     | 17 18 19 20 21 22  |
    # | P * * B . Y @     | 25 26 27 28 29 30 31
    # | P . . B . . |     | 33 34 35 36 37 38  |
    # | O . . . A A |     | 41 42 43 44 45 46  |
    # | O . . . . . |     | 49 50 51 52 53 54  |
    # | | | | | | | |     |  |  |  |  |  |  |  |
    start = (('@', (31,)),
             ('*', (26, 27)), 
             ('G', (9, 10)),
             ('Y', (14, 22, 30)), 
             ('P', (17, 25, 33)), 
             ('O', (41, 49)), 
             ('B', (20, 28, 36)), 
             ('A', (45, 46)), 
             ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
                    40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

    expected = [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]
    path = solve(start, n=8, verbose=False)
    assert actions(solve(start, n=8)) == expected

    # ----------------------------------------------

    I = inventory(start, n=8)
    s = step(state=start, specs=I)
    new, action = next(s)
    car, offset = action
    # action produced by step should be a move (car, offset)
    # resulting in new state
    assert new == move(car, offset, state=start)[0]

    # ----------------------------------------------

    # Y should only have 22 as possible spot to move
    offsets = moves(car='Y', spots=(14,22,30), state=start, specs=I)
    assert set(offsets) == set([8])

    # "*" should not have any possible moves in start state
    offsets = moves(car='*', spots=(26,27), state=start, specs=I)
    assert set(offsets) == set([])

    # ----------------------------------------------
    # step through states produced by actions ...
    # [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

    # show(start, 8)
    new, action = move(car='A', offset=-3, state=start)
    # show(new, 8, action)

    new, action = move(car='B', offset=16, state=new)
    assert action == ('B', 16)
    # show(new, 8, action)

    new, action = move(car='Y', offset=24, state=new)
    assert action == ('Y', 24)
    # show(new, 8, action)

    new, action = move(car='*', offset=4, state=new)
    assert action == ('*', 4)
    # show(new, 8, action)

    # ----------------------------------------------

    show(start, 8)
    new, action = move(car='A', offset=-3, state=start)
    new, action = move(car='Y', offset=24, state=new)
    show(new, 8, action)

    # "*" should still not have any possible moves in new state
    # since its still blocked by B
    offsets = moves(car='*', spots=(26,27), state=new, specs=I)
    assert set(offsets) == set([])

    # ----------------------------------------------

    # A should have 42, 43, and 44 as possible spots to move:
    offsets = moves(car='A', spots=(45,46), state=start, specs=I)
    assert set(offsets) == set([-3, -2, -1])

    # B should have 12, 28, and 36 as possible spots to move:
    offsets = moves(car='B', spots=(20,28,36), state=start, specs=I)
    assert set(offsets) == set([-8, 8, 16])

    # ----------------------------------------------

    car = Car(size=2, unit=(1,2,3,4), spaces=(1,2,3))
    assert car.size == 2
    assert car.unit == (1,2,3,4)
    assert car.spaces == (1,2,3)

    assert orientation((1, 2)) == 'h'
    assert orientation((0, 8)) == 'v'


    # state of cars consists of pairs of their labels and spots
    cars = (('*', (26, 27)), 
            ('G', (9, 10)),
            ('Y', (14, 22, 30)), 
            ('P', (17, 25, 33)), 
            ('O', (41, 49)), 
            ('B', (20, 28, 36)), 
            ('A', (45, 46)))

    I = inventory(cars, n=8)
    assert I['*'].size == 2
    assert I['*'].spaces == set([25, 26, 27, 28, 29, 30])
    assert I['Y'].size == 3
    assert I['Y'].spaces == set([14, 22, 30, 38])

    result = grid(cars, n=8)
    assert set(start) == set(result)

    final = (('@', (31,)),
             ('*', (30, 31)), 
             ('G', (9, 10)))
    assert done(final)
