'''Tests for our parking start functions.'''

from main import *

start = (
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

cars = (
    ('*', (26, 27)), 
    ('G', (9, 10)),
    ('Y', (14, 22, 30)), 
    ('P', (17, 25, 33)), 
    ('O', (41, 49)), 
    ('B', (20, 28, 36)), 
    ('A', (45, 46)), 
    )

def test_spots():
    '''Testing spots function'''
    assert spots(26, 2) == (26, 27)
    assert spots(10, 3, 2) == (10, 12, 14)
    assert cars == (('*', spots(26, 2)),             # ('*', (26, 27))
                    ('G', spots(9, 2)),              # ('G', ( 9, 10))
                    ('Y', spots(14, 3, 8)),          # ('Y', (14, 22, 30))
                    ('P', spots(17, 3, 8)),
                    ('O', spots(41, 2, 8)),
                    ('B', spots(20, 3, 8)),
                    ('A', spots(45, 2)))

def test_goal():
    '''Testing goal function'''
    # Should always be in middle of RH-side of grid:
    #  0  1  2  3
    #  4  5  6 [7]
    #  8  9  10 11
    #  12 13 14 15
    assert goal(4) == (7,)
    assert goal(5) == (14,)
    assert goal(6) == (17,)
    #  0  1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 [27]
    # 28 
    # 35
    # 42 43 44 45 46 47 48
    assert goal(7) == (27,)
    assert goal(8) == (31,)

def test_wall():
    '''Testing wall function'''
    assert wall(8) == (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 
                       39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)

def test_grid():
    '''Testing grid function'''
    result = grid(cars, 8)
    assert set(start) == set(result)

def test_car():
    '''Testing car representation'''
    a = Car(size=2, unit=(1,2,3,4), spaces=(1,2,3))
    b = Car(2, (1,2,3,4), (1,2,3))
    for car in (a, b):
        assert car.size == 2
        assert car.unit == (1,2,3,4)
        assert car.spaces == (1,2,3)

def test_orientation():
    '''Testing orientation function'''
    assert orientation((1, 2)) == 'h'
    assert orientation((0, 8)) == 'v'

def test_row():
    '''Testing row function'''
    #  0  1  2  3
    #  4  5  6  7 
    #  8  9  10 11
    #  12 13 14 15
    assert row(0, 4) == (0, 1, 2, 3)
    assert row(7, 4) == (4, 5, 6, 7)
    assert row(12, 4) == (12, 13, 14, 15)
    assert row(14, 4) == (12, 13, 14, 15)
    assert row(15, 4) == (12, 13, 14, 15)
    # |  |  |  |  |  |  |  |
    # |  9 10 11 12 13 14  |
    # | 17 18 19 20 21 22  |
    # | 25 26 27 28 29 30 31
    # | 33 34 35 36 37 38  |
    # | 41 42 43 44 45 46  |
    # | 49 50 51 52 53 54  |
    # |  |  |  |  |  |  |  |
    assert row(0, 8) == tuple(range(8))
    assert row(7, 8) == tuple(range(8))
    assert row(8, 8) == tuple(range(8,16))

def test_column():
    '''Testing column function'''
    #   0  1  2  3
    #   4  5  6  7 
    #   8  9  10 11
    #   12 13 14 15
    assert column(0, 4) == (0, 4, 8, 12)
    assert column(5, 4) == (1, 5, 9, 13)
    assert column(10, 4) == (2, 6, 10, 14)
    assert column(15, 4) == (3, 7, 11, 15)
    # |  |  |  |  |  |  |  |
    # |  9 10 11 12 13 14  |
    # | 17 18 19 20 21 22  |
    # | 25 26 27 28 29 30 31
    # | 33 34 35 36 37 38  |
    # | 41 42 43 44 45 46  |
    # | 49 50 51 52 53 54  |
    # |  |  |  |  |  |  |  |
    assert column(46, 8) == (6,14,22,30,38,46,54,62)
    assert column(31, 8) == (7,15,23,31,39,47,55,63)

def test_spaces():
    '''Testing spaces function'''
    # Permissible spaces for a car are based on the car's leading index
    # (the first of its spots) so we have to leave room for remaining spots.
    # Consider a car in row 2 of a 5 x 5 grid occupying, say, spots 6 and 7:
    #  |  |  |  |  |
    #  |  6  7  8  |
    #  | 11 12 13 14
    #  | 16 17 18  |
    #  |  |  |  |  | 
    # Note that the leading index of this car can only assume
    # spot 6 or 7, etc.
    print spaces((6,7), n=5)
    assert spaces((6,7), n=5) == set([6, 7])
    # But for a two-spot car in the row 3, there's an additional spot
    # available because of the extra goal space:
    assert spaces((12,13), n=5) == set([11, 12, 13])

def test_inventory():
    '''Testing inventory function'''
    #  start state ...
    # | | | | | | | |     |  |  |  |  |  |  |  |
    # | G G . . . Y |     |  9 10 11 12 13 14  |
    # | P . . B . Y |     | 17 18 19 20 21 22  |
    # | P * * B . Y @     | 25 26 27 28 29 30 31
    # | P . . B . . |     | 33 34 35 36 37 38  |
    # | O . . . A A |     | 41 42 43 44 45 46  |
    # | O . . . . . |     | 49 50 51 52 53 54  |
    # | | | | | | | |     |  |  |  |  |  |  |  |
    I = inventory(start, n=8)
    assert I['*'].size == 2
    assert I['*'].spaces == set([25, 26, 27, 28, 29, 30])
    assert I['Y'].size == 3
    assert I['Y'].spaces == set([14, 22, 30, 38])

def test_done():
    '''Testing done function'''
    state = (('@', (5,)),   # goal spot
             ('*', (3,4)))  # our car
    assert not done(state), "our car is not yet in the goal spot"

    state = (('@', (5,)),   # goal spot
             ('*', (4,5)))  # our car
    assert done(state), "our car is now in the goal spot"

    state = (('@', (31,)),      # goal spot
             ('*', (30, 31)),   # our car
             ('G', (9, 10)))    # some other car
    assert done(state), "our car is in the goal spot"

def test_occupied():
    '''Testing occupied function'''
    taken = [9,10,14,17,20,22,25,26,27,28,30,33,36,41,45,46,49]
    assert occupied(start) == set(taken)

def test_move():
    '''Testing move function'''
    #  start state ...
    # | | | | | | | |     |  |  |  |  |  |  |  |
    # | G G . . . Y |     |  9 10 11 12 13 14  |
    # | P . . B . Y |     | 17 18 19 20 21 22  |
    # | P * * B . Y @     | 25 26 27 28 29 30 31
    # | P . . B . . |     | 33 34 35 36 37 38  |
    # | O . . . A A |     | 41 42 43 44 45 46  |
    # | O . . . . . |     | 49 50 51 52 53 54  |
    # | | | | | | | |     |  |  |  |  |  |  |  |
    s = dict(start)
    assert s['A'] == (45, 46)
    state, action = move('A', offset=-3, state=start)
    s = dict(state)
    assert s['A'] == (42, 43)
    assert action == ('A', -3)

    assert s['B'] == (20, 28, 36)
    state, action = move('B', offset=16, state=start)
    s = dict(state)
    assert s['B'] == (36, 44, 52)

def test_moves():
    '''Testing moves generator'''
    #  start state ...
    # | | | | | | | |     |  |  |  |  |  |  |  |
    # | G G . . . Y |     |  9 10 11 12 13 14  |
    # | P . . B . Y |     | 17 18 19 20 21 22  |
    # | P * * B . Y @     | 25 26 27 28 29 30 31
    # | P . . B . . |     | 33 34 35 36 37 38  |
    # | O . . . A A |     | 41 42 43 44 45 46  |
    # | O . . . . . |     | 49 50 51 52 53 54  |
    # | | | | | | | |     |  |  |  |  |  |  |  |
    I = inventory(start, n=8)
    offsets = moves(car='A', spots=(45,46), state=start, specs=I)
    assert set(offsets) == set([-3, -2, -1]), "spots: 42, 43, 44"
    offsets = moves(car='B', spots=(20,28,36), state=start, specs=I)
    assert set(offsets) == set([-8, 8, 16]), "spots: 12, 38, 36"
    offsets = moves(car='Y', spots=(14,22,30), state=start, specs=I) 
    assert set(offsets) == set([8]), "spots: 22"
    offsets = moves(car='G', spots=(9,10), state=start, specs=I) 
    assert set(offsets) == set([1,2,3]), "spots: 10, 11, 12"
    offsets = moves(car='P', spots=(17,25,33), state=start, specs=I) 
    assert set(offsets) == set([]), "spots: None"

def test_step():
    '''Testing step generator'''
    #  start state ...
    # | | | | | | | |     |  |  |  |  |  |  |  |
    # | G G . . . Y |     |  9 10 11 12 13 14  |
    # | P . . B . Y |     | 17 18 19 20 21 22  |
    # | P * * B . Y @     | 25 26 27 28 29 30 31
    # | P . . B . . |     | 33 34 35 36 37 38  |
    # | O . . . A A |     | 41 42 43 44 45 46  |
    # | O . . . . . |     | 49 50 51 52 53 54  |
    # | | | | | | | |     |  |  |  |  |  |  |  |
    I = inventory(start, n=8)
    s = step(state=start, specs=I)
    new, action = next(s)
    # new should be the new state resulting from action
    # and action should be a move (car, offset)
    car, offset = action
    assert new == move(car, offset, state=start)[0]

def test_solve():
    '''Testing solve function'''
    expected = [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]
    path = solve(start, n=8, verbose=False)
    assert actions(solve(start, n=8)) == expected
