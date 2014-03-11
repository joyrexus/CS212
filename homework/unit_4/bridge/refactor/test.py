'''
Tests for bridge problem modules.

'''
from search import *
from main import *

def test_path():
    '''Testing Path class'''
    x = Path('a', 'b', 'c')
    y = Path('d', 'e', 'f')
    assert x[0] is 'a'
    assert x[-1] is 'c'
    assert x.first is 'a'
    assert x.last is 'c'
    assert y[0] is 'd'
    assert y[-1] is 'f'
    assert y.first is 'd'
    assert y.last is 'f'

    r = State(cost=1)
    q = State(cost=2)
    x = State(cost=4)
    y = State(cost=6)
    # paths are comparable by the cost attribute of their last state
    assert Path(x,y) > Path(q) > Path(r), 'comparing by cost'
    assert Path(r) < Path(q) < Path(x,y), 'comparing by cost'

def test_paths():
    '''Testing PathList class'''
    x = Path('a', 'b', 'c')
    y = Path('d', 'e', 'f')
    P = PathList(x, y)
    assert P.first is x
    assert P.last is y

    r = State((1,2), cost=1)
    q = State((1,2), cost=2)
    x = State((3,4), cost=4)
    y = State((5,6), cost=6)
    paths = PathList(Path(x,y))
    assert paths.first == Path(x,y)
    assert paths.last == Path(x,y)

    paths.add(Path(q))
    assert paths.first == Path(q), "q is first due to lower cost"
    assert paths.last == Path(x,y)
    assert paths.cost == 6

    paths.add(Path(r))
    assert paths.first == Path(r), "r replaces q (same state, lower cost)"
    assert paths.last == Path(x,y)

    A = Path(x,y)
    B = Path(q)
    assert A.cost == 6
    assert B.cost == 2
    paths = PathList(A, B)
    assert paths.cost == 2, "cost of last path"

def test_side():
    '''Testing Side class'''
    L = Side(1, 4, 5)
    R = Side()
    assert L == frozenset([1,4,5]) == Side(1, 4, 5)
    assert R == frozenset([])

def test_action():
    '''Testing Action class'''
    action = Action(2, 1)
    assert action.crossing == set([2, 1])
    assert action.cost == 2

def test_state():
    '''Testing State class'''
    start = (1, 4, 5)
    state = State(start)
    assert state == State(left=[1,4,5], cost=0)
    assert state.right == frozenset([]) == Side()

def test_next():
    '''Testing next method'''
    Z = frozenset

    start = State(left=[1])
    expected = set([State(right=[1], light='R', action=[1])])
    assert next(start) == expected

    start = State(left=[1,2], right=[3])
    expected = set([
        State(left=[2], right=(1,3), light='R', action=[1]),
        State(left=[1], right=(2,3), light='R', action=[2]),
        State(right=(1,2,3), light='R', action=[1,2]) 
    ])
    assert next(start) == expected

def test_solve():
    '''Testing solve method'''
    expected = [
        State(left=[1]),
        State(right=[1], light='R', action=[1], cost=1)
    ]
    assert solve(1) == expected

    expected = [
        State(left=[1,2]),
        State(right=[1,2], light='R', action=(1,2), cost=2)
    ]
    assert solve(1,2) == expected

    expected = [
        State(left=(1,2,5,10)),
        State(left=(5,10), light='R', right=(1,2), action=(2,1), cost=2),
        State(left=(2,5,10), right=[1], action=[2], cost=4),
        State(left=[2], right=(1,5,10), light='R', action=[5,10], cost=14),
        State(left=(1,2), right=(5,10), action=[1], cost=15),
        State(right=(1,2,5,10), light='R', action=(1,2), cost=17)
    ]
    result = solve(1, 2, 5, 10)
    assert isinstance(result, Path)
    assert result.cost == 17
    assert result == expected
