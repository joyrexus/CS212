from __future__ import division
from collections import defaultdict


def solve(words):
    '''
    Return any of the highest scoring portmanteau words formed from
    any two of the list of words.

    (start + mid + end), where both (start + mid) and 
    (mid + end) are among the list of words passed in.  

    '''
    scores = defaultdict(int)
    for x in words:
        for y in words:
            if x == y: continue
            for a, b in splits(x):
                if y.startswith(b) and len(b) != len(y):
                    c = y[len(b):]
                    w = "{0}{1}{2}".format(a, b, c)
                    scores[score(a, b, c)] = w
    return scores[max(scores)] if scores else None


def splits(word):
    '''Return list of word splits.'''
    return [(word[:i], word[i:]) for i in range(1, len(word))]


def score(A, B, C):
    '''Return score of word.'''
    a = len(A)      # start
    b = len(B)      # mid
    c = len(C)      # end
    w = a + b + c   # length of candidate word
    q = w / 4       # preferred length of start
    r = w / 2       # preferred length of mid
    s = w / 4       # preferred length of end
    return w - abs(a-q) - abs(b-r) - abs(c-s)


if __name__ == '__main__':
    '''
    Tests for score and solve functions.
    
    '''
    assert score(A='adole', B='scent', C='ed') == 8

    assert solve(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')

    assert solve(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'

    assert solve(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'

    assert solve(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'

    assert solve(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'

    assert solve(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'

    assert solve(['morass', 'moral', 'assassination']) == 'morassassination'

    assert solve(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')

    assert solve(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'

    assert solve(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'

    assert solve(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'

    assert solve([]) == None
    assert solve(['']) ==  None
    assert solve(['test']) == None
    assert solve(['ABC', '123']) == None
    assert solve(['dog', 'dogs']) == None
    assert solve(['night', 'day']) == None

