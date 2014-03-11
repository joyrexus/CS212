# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

from collections import defaultdict

def is_palind_simple(text):
    text = text.lower()
    return text == text[::-1]

def is_palind(text):
    text = text.lower()
    L = len(text)
    for i in range((L/2) + 1):
        j = L - i - 1
        if j > 0 and not text[i] == text[j]:
            return False
    return True


def test_is_palind():
    P = is_palind_simple
    assert P('xxx')
    assert P('x x')
    assert P('yx xy')
    assert P('yx z z xy')
    assert P('')
    assert not P('xxy')
    assert P('racecar')
    assert P('Racecar')
    assert not P('racecarX')
    print "is_palind tests passed"

# test_is_palind()

def size(a, b): return b - a

def longest(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    text = text.lower()
    MAX = (0, 0)
    for i in range(len(text)):
        for j in (i, i+1):
            prospect = expand(text, i, j)
            if size(*prospect) > size(*MAX):
                MAX = prospect 
    return MAX

def expand(text, i, j):
    while (i >= 0 and j < len(text) and text[i] == text[j]):
            i -= 1
            j += 1
    return (i+1, j)
                

def test_longest():
    L = longest
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

test_longest()
