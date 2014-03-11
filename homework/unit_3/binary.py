from bisect import bisect_right

def closest(seq, x):
    '''Return value less than or equal to x.'''
    i = bisect_right(seq, x)
    return seq[i-1]

print closest(range(10), 5.2)


