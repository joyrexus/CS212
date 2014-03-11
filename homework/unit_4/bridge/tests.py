from bridge import bridge_problem, elapsed_time
import doctest

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


class TestBridge: """

>>> elapsed_time(bridge_problem([1,2,5,10]))
17

>>> p = (bridge_problem([1,2,5,10]))
>>> len(path_states(p)) == len(path_actions(p)) + 1
True

>>> bridge_problem([1,2,5,10]) == bridge_problem([10,5,2,1])
True

>>> actions = [(2, 1, '->'), (1, 1, '<-'), (3, 1, '->')]
>>> path_actions(bridge_problem([1,2,3])) == actions
True

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

"""

print doctest.testmod()
