from util.deco import memo, trace, countcalls

@countcalls
@trace
@memo
def fib(n):
    '''Return fibonacci number for n.'''
    return 1 if n <= 1 else fib(n-1) + fib(n-2)

print fib.__doc__
fib(8)
print fib.calls, 'calls made'
