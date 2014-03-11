from __future__ import division


sects = '20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5'.split()
extra = sects + [20]
neighbors = dict((x, (sects[i-1], extra[i+1])) for i,x in enumerate(sects))

def sect_dist(target, miss):
    '''
    Return a probability distribution of [(sect, prob)] pairs.

    Half the miss rate goes to one of the target section's neighbors
    and the other half to its other neighbor.  (See the neighbors dict.)

    >>> sect_dist('S20', .2)
    {'1': 0.1, '5': 0.1, '20': 0.8}

    '''
    ring = target[0]
    sect = target[1:]
    if sect == 'B': 
        ratio =  miss/20                # misses get evenly distributed
        dist = [(s, ratio) for s in sects] + [('B', 1 - miss)]
        return dict(dist)
    else:
        (left, right) = neighbors[sect]
        return dict([(left, miss * .5), (right, miss * .5), (sect, 1 - miss)])


def outcome(target, miss):
    '''
    Return a probability distribution of [(target, prob)] pairs.
    
    >>> outcome('S20', .2)
    {'D20': 0.016, 'S1': 0.096, ... }

    '''
    pass


if __name__ == '__main__':

    assert sect_dist('S20', .2) == {'1': 0.1, '5': 0.1, '20': 0.8}

    expected = {'B': 0.8, '11': 0.01, '10': 0.01, '13': 0.01, '20': 0.01, 
                '14': 0.01, '17': 0.01, '16': 0.01, '19': 0.01, '18': 0.01, 
                '1': 0.01, '3': 0.01, '2': 0.01, '5': 0.01, '4': 0.01, '7': 0.01, 
                '6': 0.01, '9': 0.01, '15': 0.01, '12': 0.01, '8': 0.01}
    assert sect_dist('SB', .2) == expected

    raise SystemExit

    expected = {'D20': 0.016, 'S1': 0.096, 'T5': 0.002, 'S5': 0.096, 
                'T1': 0.002, 'S20': 0.768, 'T20': 0.016, 'D5': 0.002, 'D1': 0.002}
    assert outcome('S20', .2) == expected
