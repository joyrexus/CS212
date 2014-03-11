import functools
from functools import update_wrapper, wraps

def decorator(deco):
    '''
    Decorate a decorator so that it inherits the docstrings 
    and stuff from the function it's decorating.

    '''
    def wrapped(f):
        return update_wrapper(deco(f), f)
    update_wrapper(wrapped, deco)
    return wrapped

@decorator
def countcalls(f):
    '''Decorator that counts calls made to the function decorated.'''
    def counted(*args):
        counted.calls = getattr(counted, 'calls', 0) + 1
        return f(*args)
    return counted

@decorator
def memo(f):
    '''
    Memoize a function so that it caches all return values for 
    faster future lookups.

    '''
    cache = {}
    def memoized(*args):
        update_wrapper(memoized, f)
        if args in cache:
            return cache[args]
        else:
            result = cache[args] = f(*args)
            return result
    return memoized

@decorator
def n_ary(f):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    
    '''
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args)) 
    return n_ary_f

@memo
@countcalls
@n_ary
def foo(a, b):
    '''A little test function.'''
    return a + b

print foo(4, 3)
print foo(4, 3, 2)
print foo(4, 3)
print "foo was called", foo.calls, "times"

@countcalls
@memo
@n_ary
def bar(a, b):
    '''A little test function.'''
    return a + b

print bar(4, 3)
print bar(4, 3, 2)
print bar(4, 3, 2, 1)
print "bar was called", bar.calls, "times"
