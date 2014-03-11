def outcome(target, miss):
    '''
    Return a probability distribution of [(target, probability)] pairs.
    
    '''
    pass


def best_target(miss):
    '''Return the target that maximizes the expected score.'''
    pass
    

def same_outcome(a, b):
    '''
    Two states a and b are the same if all corresponding sets 
    of locs are the same.

    '''
    return all(abs(a.get(key, 0) - b.get(key, 0)) <= 0.0001
               for key in set(a) | set(b))


if __name__ == '__main__':

    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'

    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})

    expected = {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                'S5': 0.005, 'T1': 0.045, 'S20': 0.09}
    assert same_outcome(outcome('T20', 0.1), expected)

    expected = {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 
                'S1': 0.016, 'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 
                'S4': 0.016, 'S20': 0.016, 'S19': 0.016, 'S18': 0.016, 
                'S13': 0.016, 'S12': 0.016, 'S11': 0.016, 'S10': 0.016, 
                'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
                'S7': 0.016, 'SB': 0.64}
    assert same_outcome(outcome('SB', 0.2), expected)

