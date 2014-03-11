import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    times = []
    if type(n) is int:
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        start, last = time.clock(), 0
        while last - start <= n:
            times.append(timedcall(fn, *args)[0])
            last = time.clock()
    return min(times), average(times), max(times)


def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)
def ffact(n):
    return 1 if n <= 1 else fact(n) * ffact(n - 1)


print timedcall(ffact, 50)
print timedcalls(10, ffact, 50)
