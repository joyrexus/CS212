from main import *

def test_glass():
    '''Testing Glass class'''
    g = Glass(0, 5)
    assert g.level == 0
    assert g.total == 5

def test_glasses():
    '''Testing Glasses class'''
    glasses = Glasses([Glass(level=3, total=5), 
                       Glass(level=0, total=10)])
    assert glasses.empty(0)  == (Glass(0,5), Glass(0,10))
    assert glasses.fill(1)   == (Glass(3,5), Glass(10,10))
    assert glasses.pour(0,1) == (Glass(0,5), Glass(3,10))

def test_state():
    '''Testing State class'''
    glasses = Glasses([Glass(3,5), Glass(0,10)])
    state = State(glasses, action=None)
    assert state.contains(3)
    assert state.contains(0)
    assert not state.contains(1)

def test_next():
    '''Testing next method'''
    glasses = Glasses([Glass(3,5), Glass(0,7)])
    state = State(glasses, action=None)
    expected = set([
        State((Glass(3,5), Glass(0,7)), action=('pour',1,0)),
        State((Glass(3,5), Glass(7,7)), action=('fill',1)),
        State((Glass(5,5), Glass(0,7)), action=('fill',0)), 
        State((Glass(0,5), Glass(3,7)), action=('pour',0,1)),
        State((Glass(3,5), Glass(0,7)), action=('empty',1)), 
        State((Glass(0,5), Glass(0,7)), action=('empty',0))
    ])
    assert next(state) == expected

def test_state():
    '''Testing solve method'''
    start = State(Glasses([Glass(0,1), 
                           Glass(0,2), 
                           Glass(0,4),
                           Glass(0,8)]), action=None)
    stop = State(Glasses([Glass(0,1), 
                          Glass(0,2), 
                          Glass(4,4),
                          Glass(0,8)]), action=('fill', 2))
    assert stop.contains(4)
    assert solve(totals=(1,2,4,8), goal=4) == [start, stop]
