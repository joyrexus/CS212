from __future__ import division
from collections import defaultdict


# dict of ring, function pairs
# each ring's function returns a prob dist given the miss ratio
ring_model = {
    'T':  lambda miss: (('S', miss), ('T', 1 - miss)),
    'D':  lambda miss: (('S', miss*.5), ('OFF', miss*.5)),
    'S':  lambda miss: (('D', miss*.1), ('T', miss*.1), ('S', 1 - miss*.2)),
    'SB': lambda miss: (('S', miss*.75), ('DB', miss*.25), ('SB', 1 - miss)),
    'DB': lambda miss: (('S', miss * 3 * (2/3)), 
                        ('SB', miss * 3 * (2/3)),
                        ('DB', 1 - miss * 3))
}

def ring_dist(target, miss):
    '''
    Return a dict-based probability distribution of [(ring, prob)] pairs.

    We're just doing a lookup in the ring model for the right distribution
    function and passing that function the miss ratio.

    >>> ring_dist('S20', .2)
    {'S': 0.96, 'D': 0.02, 'T': 0.02}

    '''
    ring = target[0]
    sect = target[1:]
    if sect == 'B': ring = target
    dist = ring_model[ring](miss)
    return dict(((r, round(m, 3)) for r,m in dist))


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

    DB 1 ...
    S1 0.05 0.01
       ^^^^
    SB 1 ...
    S1 0.8 0.01
       ^^^
    S B ...
    S1 0.15 0.8
       ^^^^

    '''
    target_dist = defaultdict(float)
    for ring, r in ring_dist(target, miss).items():
        for sect, s in sect_dist(target, miss).items():
            if ring == 'S' and sect.endswith('B'):
                for i in sects:
                    t = name(ring, i)
                    target_dist[t] += (r * s) / 20.0
            else:
                t = name(ring, sect)
                target_dist[t] += r * s
    return target_dist

def name(ring, sect):
    '''Construct a target name from a ring and section.'''
    if ring == 'OFF':
        return 'OFF'
    elif ring in ('SB', 'DB'):
        return ring if (sect == 'B') else ('S' + sect)
    else:
        return ring + sect


if __name__ == '__main__':

    target = 'SB'  # target name
    miss = 0.2      # miss ratio
    assert ring_dist(target, miss) == {'SB': 0.8, 'S': 0.15, 'DB': 0.05}
    expected = {'B': 0.8, '11': 0.01, '10': 0.01, '13': 0.01, '20': 0.01, 
                '14': 0.01, '17': 0.01, '16': 0.01, '19': 0.01, '18': 0.01, 
                '1': 0.01, '3': 0.01, '2': 0.01, '5': 0.01, '4': 0.01, 
                '7': 0.01, '6': 0.01, '9': 0.01, '15': 0.01, '12': 0.01, 
                '8': 0.01}
    assert sect_dist(target, miss) == expected
    expected = {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 
                'S1': 0.016, 'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 
                'S4': 0.016, 'S20': 0.016, 'S19': 0.016, 'S18': 0.016, 
                'S13': 0.016, 'S12': 0.016, 'S11': 0.016, 'S10': 0.016, 
                'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
                'S7': 0.016, 'SB': 0.64}

    results = outcome(target, miss)
    for t, p in results.items(): 
        print t, p, expected[t], p == expected[t]
    assert results == expected
    raise SystemExit

    # -------------------------------------------------------------------

    target = 'S20'  # target name
    miss = 0.2      # miss ratio
    assert ring_dist(target, miss) == {'S': 0.96, 'D': 0.02, 'T': 0.02}
    assert sect_dist(target, miss) == {'1': 0.1, '5': 0.1, '20': 0.8}

    expected = {'D20': 0.016, 'S1': 0.096, 'T5': 0.002, 'S5': 0.096, 
                'T1': 0.002, 'S20': 0.768, 'T20': 0.016, 'D5': 0.002, 
                'D1': 0.002}
    assert outcome(target, miss) == expected
