from main import *

def test_subway():
    '''Testing subway function'''
    expected = {
        'a': {'b': 'blue'}, 
        'x': {'c': 'blue', 'b': 'green'}, 
        'c': {'x': 'blue', 'b': 'blue', 'z': 'green'}, 
        'b': {'a': 'blue', 'x': 'green', 'c': 'blue', 'z': 'green'}, 
        'z': {'c': 'green', 'b': 'green'}
    }
    assert subway(blue='a b c x', green='x b z c') == expected

def test_boston():
    '''Testing boston system map'''
    assert boston['state'] == dict(downtown='orange', 
                                   haymarket='orange', 
                                   aquarium='blue', 
                                   government='blue')

def test_ride():
    '''Testing ride function'''
    expected = ['mit', 'red', 'charles', 'red', 'park']
    assert ride('mit', 'park') == expected

    expected = ['mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mit', 'government') == expected

    expected = ['mattapan', 'red', 'umass', 'red', 'south', 'red', 
                'downtown', 'orange', 'chinatown', 'orange', 
                'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('mattapan', 'foresthills') == expected

def test_longest():
    '''Testing longest_ride function'''
    A = ['wonderland', 'revere', 'suffolk', 'airport', 'maverick', 
         'aquarium', 'state', 'downtown', 'park', 'charles', 'mit', 
         'central', 'harvard', 'porter', 'davis', 'alewife']
    B = ['alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 
         'charles', 'park', 'downtown', 'state', 'aquarium', 
         'maverick', 'airport', 'suffolk', 'revere', 'wonderland']
    result = path_states(longest_ride(boston)) 
    assert result in (A, B)
    assert len(result) == 16
