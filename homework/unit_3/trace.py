from functools import update_wrapper

def disable(f): 
    '''
    Disable a decorator by re-assigning the decorator's name 
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return f

def decorator(d):
    '''Make function d a decorator: d wraps a function f.'''
    def _d(f):
        return update_wrapper(d(f), f)
    update_wrapper(_d, d)
    return _d

@decorator
def countcalls(f):
    '''Counts calls made to the function decorated.'''
    def counted(*args):
        counted.calls = getattr(counted, 'calls', 0) + 1
        return f(*args)
    return counted

@decorator
def trace(f, spaces='    '):
    '''Trace calls made to function decorated.'''
    def _f(*args):
        signature = '{0}({1})'.format(f.__name__, ', '.join(map(repr, args)))
        indent = trace.level * spaces
        print '{0} --> {1}'.format(indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            indent = (trace.level-1) * spaces
            print '{0} <-- {1} == {2}'.format(indent, signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

@decorator
def memo(f):
    '''
    Memoize a function so that it caches all return values for 
    faster future lookups.

    '''
    def memoized(*args):
        if not getattr(memoized, 'cache', None):
            memoized.cache = {}
        if args in memoized.cache:
            return memoized.cache[args]
        else:
            result = memoized.cache[args] = f(*args)
            return result
    return memoized

if __name__ == '__main__':

    # trace = disable

    @countcalls
    @trace
    @memo
    def fib(n):
        '''Return fibonacci number for n.'''
        return 1 if n <= 1 else fib(n-1) + fib(n-2)

    fib(8)
    print fib.calls, 'calls made'
