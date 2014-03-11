******************
The Parking Puzzle
******************

This problem tests your knowledge of searching for optimal paths as covered in
unit 4.


Overview
========

The optimal paths we're interested in for this problem are a series
of car moves through a parking lot.

The solver we're going to write can be thought of as a parking director
orchestrating traffic in his lot.  The director's job is to get your
car onto a designated goal spot as efficiently as possible.  That is,
to get your car onto the goal spot will likely require moving a number
of other cars (to get them out of the way) and he wants to do this 
by minimizing the number of moves.

So, the solver function is going to take a particular parking puzzle
as input (the starting state of the parking lot).  It should return the
shortest path to the goal state.  The path will consist of a series of 
states (starting state, transitional states, and the final goal state) 
and actions (car moves resulting in a new state).

Note, these states are just representations of a particular state of the 
parking lot: a given configuration of cars within the lot.


Representations
===============

A parking lots consists of walls, cars, and spaces (empty spots).

We're going to represent a particular state of the lot with grid diagrams 
like the following::

    | | | | | | | |  
    | G G . . . Y |  
    | P . . B . Y | 
    | P * * B . Y @ 
    | P . . B . . |  
    | O . . . A A |  
    | O . S S S . |  
    | | | | | | | | 

``|`` represents a wall around the parking lot.

``*`` represents your car.

``A`` (and all other letters) represents a car.

``.`` represents an empty spot.

``@`` marks a goal spot.

Cars are either long (3 spots) or short (2 spots) and can only move in the 
direction they are pointing.  

In the puzzle represented above, the cars GG, AA, SSS, and ** are horizontally 
oriented, so they can move any number of squares right or left, as long as 
they don't bump into another car or wall.  

So, for the horizontally oriented cars:

* GG can move 1, 2, or 3 spots to the right
  
* AA can move 1, 2, or 3 spots to the left
  
* ``**`` cannot move at all

For the vertically oriented cars:
  
* BBB can move one up or down

* YYY can move one down

* PPP and OO cannot move

------------------------------------------------------------

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format::

    puzzle = (
    ('@', (31,)),
    ('*', (26, 27)), 
    ('G', (9, 10)),
    ('Y', (14, 22, 30)), 
    ('P', (17, 25, 33)), 
    ('O', (41, 49)), 
    ('B', (20, 28, 36)), 
    ('A', (45, 46)), 
    ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
            40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

A solution to this puzzle is as follows::

    path = solve_parking_puzzle(puzzle, N=8)
    path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

That is ... 

* move ``A`` left 3
* move ``B`` down 2
* move ``Y`` down 2 
* move ``*`` right 4 (onto the goal spot)


Note that when submitting your solution, the grader checks for the following:

1. The solver you submit should return the *shortest path* to the goal state
   -- the fewest number of car moves to get your car onto the goal spot.

2. The shortest path returned should be a list containing the initial state
   and the goal state.  Each intermediate state in the path should be preceded
   by the action (car move) resulting in the new state:   
   ``[start, action1, state2, action2, ..., final]``
   
3. Actions are checked to make sure they are valid ways to move between
   the two adjacent states.


Specifics
=========

Your task is to define the function ``solve_parking_puzzle``::

    N = 8

    def solve_parking_puzzle(start, N=N):
        '''
        Return solution path for parking puzzle described by `start`.

        The `start` arg is the starting state of the puzzle specifying
        the location of cars, walls, empty spaces, and goal space.

        The starting state is represented as a tuple of object, location pairs.

        Puzzles are configurations of objects: cars, spaces, walls.

        A   cap letters represent cars
        *   our car
        @   target space
        .   empty space
        |   wall

        Return a solution path of [state, action, ...] alternating items, where
        the final state describes the locations of the puzzle objects such that
        the location of our car contains the index of the goal space and the 
        preceding states and actions describe the path (intermediate states
        and transition actions) used to reach that state.

        An action is a pair (object, distance_moved), such as ('B', 16) to move 
        'B' two squares down on the N=8 grid.
        
        '''
        

You'll define a *grid* function for representing states of the parking lot in a
well-defined format.

A pre-defined *show* function is given to visualize parking lot states given
a grid representation.

Here we see the *grid* and *spots* (née *locs*) functions in use::

    puzzle1 = grid((
        ('*', spots(26, 2)),             # ('*', (26, 27))
        ('G', spots(9, 2)),              # ('G', ( 9, 10))
        ('Y', spots(14, 3, N)),          # ('Y', (14, 22, 30))
        ('P', spots(17, 3, N)),
        ('O', spots(41, 2, N)),
        ('B', spots(20, 3, N)),
        ('A', spots(45, 2))))

    puzzle2 = grid((
        ('*', spots(26, 2)),
        ('B', spots(20, 3, N)),
        ('P', spots(33, 3)),
        ('O', spots(41, 2, N)),
        ('Y', spots(51, 3))))

    puzzle3 = grid((
        ('*', spots(25, 2)),
        ('B', spots(19, 3, N)),
        ('P', spots(36, 3)),
        ('O', spots(45, 2, N)),
        ('Y', spots(49, 3))))


Here are the *shortest_path_search* and *path_actions* functions from unit 4.
You may use these if you want, but you don't have to::

    def shortest_path_search(start, successors, is_goal):
        '''
        Find the shortest path from start state to a state
        such that is_goal(state) is true.

        '''
        if is_goal(start):
            return [start]
        explored = set()        # set of states we have visited
        frontier = [ [start] ]  # ordered list of paths we have blazed
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

    def path_actions(path):
        "Return a list of actions in this path."
        return path[1::2]


Notes
=====

As noted above, for this problem we're representing parking lots as grids with 
integer indices.  Here are the indices of the spots in a 4 x 4 lot::

    0  1  2  3
    4  5  6 (7) 
    8  9  10 11
    12 13 14 15

Note that we always place the goal spot in the middle of the right-hand side
of the perimeter of the grid -- at index 7 in the lot above.

Here we see the non-wall index numbers (with the goal at index 31)::

    |  |  |  |  |  |  |  |
    |  9 10 11 12 13 14  |
    | 17 18 19 20 21 22  |
    | 25 26 27 28 29 30 31
    | 33 34 35 36 37 38  |
    | 41 42 43 44 45 46  |
    | 49 50 51 52 53 54  |
    |  |  |  |  |  |  |  |

Here's a representation of a particular parking lot state alongside the 
grid indices::

    | | | | | | | |     |  |  |  |  |  |  |  |
    | G G . . . Y |     |  9 10 11 12 13 14  |
    | P . . B . Y |     | 17 18 19 20 21 22  |
    | P * * B . Y @     | 25 26 27 28 29 30 31
    | P . . B . . |     | 33 34 35 36 37 38  |
    | O . . . A A |     | 41 42 43 44 45 46  |
    | O . . . . . |     | 49 50 51 52 53 54  |
    | | | | | | | |     |  |  |  |  |  |  |  |

This representation of a state (the left-hand side diagram) can be generated 
with the *show* function given the grid-format produced by the *grid* function.

Here's a sample starting state, based on the representation above::

    start = (('@', (31,)),
             ('*', (26, 27)), 
             ('G', (9, 10)),
             ('Y', (14, 22, 30)), 
             ('P', (17, 25, 33)), 
             ('O', (41, 49)), 
             ('B', (20, 28, 36)), 
             ('A', (45, 46)), 
             ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,

Given this starting state, our solver should return the shortest path
to the goal state.  Here are the actions from the resulting shortest path
given our starting state::

    path = solve_parking_puzzle(start, N=8)
    path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
and finally '*' moves 4 spaces right to the goal.

As indicated above, actions are represented as pairs consisting of 
(car, offset), where the offset indicates how much the starting index
of car was offset to move it to the new state.

Here's the resulting final state::

    final = (('@', (31,)),
             ('*', (30, 31)), 
             ('G', (9, 10)),
             ('Y', (38, 46, 54)), 
             ('P', (17, 25, 33)), 
             ('O', (41, 49)), 
             ('B', (36, 44, 52)), 
             ('A', (42, 43)), 
             ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
                    40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

    | | | | | | | |
    | G G . . . . |
    | P . . . . . |
    | P . . . . * *
    | P . . B . Y |
    | O A A B . Y |
    | O . . B . Y |
    | | | | | | | |

