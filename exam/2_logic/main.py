"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.

10. Knuth arrived the day after the manager.

11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

_ = None
people = ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']
(H, K, M, S, W) = people

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    orders = list(itertools.permutations(people))
    result = next((mon, tue, wed, thu, fri)
        for (mon, tue, wed, thu, fri) in orders
        for (programmer, writer, manager, designer, _) in orders
        if manager is S 
            and s_then_k(mon, tue, wed, thu, fri)
            and programmer is not W     # and programmer is H
            and writer is not M
            and thu is not designer
            and (mon is W or writer is W)
        for (laptop, tablet, droid, iphone, _) in orders
        if droid in (W, H) 
            and programmer in (W, H)
            and droid is not programmer
            and tue in (iphone, tablet)
            and wed is laptop
            and fri is not tablet
            and designer is not droid
            and manager not in (tablet, K)
            and mon in (laptop, W) 
            and writer in (laptop, W)
            and mon is not writer)
    return list(result)


def s_then_k(*days):
    '''Knuth should immediately follow Simon.'''
    s = days.index(S)
    k = days.index(K)
    return k - s == 1

print logic_puzzle()

# ('Wilkes', 'Hamming', 'Minsky', 'Simon', 'Knuth')
#
# simon is manager since ...
# if follows(S, K)
# if follows(manager, K)
