def foo(n):
    return set(j for i in range(n) for j in range(i))

def bar(n):
    return set().union(*map(range, range(n)))

for i in range(10):
    assert foo(i) == bar(i)
