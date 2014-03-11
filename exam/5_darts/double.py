from collections import defaultdict

targets = defaultdict(list)         # given points, which targets?
doubles = defaultdict(list)         # given points, which double targets?
points = {'SB': 25, 'DB': 50}       # given target, how many points?
rings = {1: "S", 2: "D", 3: "T"}

def name(ring, sect):
    'Return string representation of target based on ring, sect values.'
    sect = 'B' if sect == 25 else str(sect)
    return rings[ring] + sect

for sect in range(1, 21):
    for ring in (1, 2, 3):
        p = sect * ring             # target's point score
        t = name(ring, sect)        # target name as string
        points[t] = p               # store points for target
        targets[p].append(t)
        if ring == 2: doubles[p].append(t)

targets[25].append('SB')
targets[50].append('DB')
doubles[50].append('DB')
scores = sorted(targets, reverse=True)          # possible scores for a target
# scores = [0] + sorted(targets, reverse=True)  # possible scores for a target

def target(score):
    '''Return list of targets with given point score.'''
    return targets.get(score, [None])[0]

def double(score):
    '''Return list of double-point targets with given point score.'''
    return doubles.get(score, [None])[0]

def score(target):
    '''Return point score for target.'''
    return points[target]

def double_out(total):
    '''
    Return any one of the shortest possible lists of targets 
    (ring/section intersections) that add to total.

    Constraints:
    1. The last dart must be a double.
    2. You can't use more than three darts.
    3. If there is no solution, return None.

    '''
    for x in scores:
        for y in scores:
            if x + y == total and double(y):
                return [target(x), double(y)]
            else:
                d = total - (x + y)
                if double(d):
                    return [target(x), target(y), double(d)]



if __name__ == '__main__':

    print double_out(2)

    #                 170  ==    60   + 60  + 50
    assert double_out(170) == ['T20', 'T20', 'DB']

    assert double_out(171) == None

    #                 100  is    (60  +  40) or (50 + 50)
    assert double_out(100) in (['T20', 'D20'], ['DB','DB'])

    for total in [0, 1, 159, 162, 163, 165, 166, 168, 169, 171, 200]:
        assert double_out(total) == None

    def valid_out(darts, total):
        "Does this list of targets achieve the total, and end with a double?"
        return (0 < len(darts) <= 3 and darts[-1].startswith('D')
                and sum(map(value, darts)) == total)

    def value(target):
        "The numeric value of a target."
        if target == 'OFF': return 0
        ring, section = target[0], target[1:]
        r = 'OSDT'.index(target[0])
        s = 25 if section == 'B' else int(section)
        return r * s

    for total in range(2, 159) + [160, 161, 164, 167, 170]:
        # assert valid_out(double_out(total), total)
        pass

