# Write a function, csuccessors, that takes a state (as defined below) 
# as input and returns a dictionary of {state:action} pairs. 
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where 
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings: 
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C'
# where 'MM->' means two missionaries travel to the right side.
# 
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """
    Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.
    
    """
    M1, C1, B1, M2, C2, B2 = state
    assert B1 is 1 or B2 is 1
    pairs = {} 
    ops = [(0,1), (1,0), (1,1), (2,0), (0,2)]
    if C1 > M1 or C2 > M2: return pairs         # more cannibals than missionaries
    if B1 is 1:
        B1, B2 = 0, 1
        for m, c in ops:
            if M1 - m >= 0 and C1 - c >= 0:
                state = (M1-m, C1-c, B1, M2+m, C2+c, B2)
                action = 'M' * m + 'C' * c + '->'
                pairs[state] = action
    else:
        B1, B2 = 1, 0
        for m, c in ops:
            if M2 - m >= 0 and C2 - c >= 0:
                state = (M1+m, C1+c, B1, M2-m, C2-c, B2)
                action = '<-' + 'M' * m + 'C' * c
                pairs[state] = action
    return pairs



def test():
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',  \
                                               (1, 2, 0, 1, 0, 1): 'M->',  \
                                               (0, 2, 0, 2, 0, 1): 'MM->', \
                                               (1, 1, 0, 1, 1, 1): 'MC->', \
                                               (2, 0, 0, 0, 2, 1): 'CC->'}

    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',  \
                                               (2, 1, 1, 3, 3, 0): '<-M',  \
                                               (3, 1, 1, 2, 3, 0): '<-MM', \
                                               (1, 3, 1, 4, 1, 0): '<-CC', \
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    return 'tests pass'

print test()
