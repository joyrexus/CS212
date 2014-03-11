from itertools import combinations
from collections import defaultdict

diffs = defaultdict(list)

letter = 'E'
n = 0
for i, j in combinations([1, 5, 7, 11, 12], 2):
    n += 1
    diffs[j-i].append((letter, i,j))
    
print diffs
print n
