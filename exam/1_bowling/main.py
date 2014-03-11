"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.

(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.

(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.

(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)

For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""
from collections import defaultdict

def bowl(balls, verbose=False):
    "Compute the total score for a player's game of bowling."
    frame, roll, prev, score = 1, 1, 0, 0
    for i, pins in enumerate(balls):
        score += pins
        if frame == 10: continue        # last frame!
        if verbose:
            print 'frame', frame
        if pins == 10 and roll == 1:
            frame += 1
            score += balls[i+1]
            score += balls[i+2]
            prev, roll = 0, 1
        elif prev + pins == 10:
            frame += 1
            score += balls[i+1]
            prev, roll = 0, 1
        elif roll == 1:
            roll, prev = 2, pins
        else:
            frame += 1
            prev, roll = 0, 1
        if verbose:
            print 'index', i
            print 'pins', pins
            print 'score', score
            print
    return score

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    frame, roll, prev, score = 1, 1, 0, 0
    for i, pins in enumerate(balls):
        score += pins
        if frame == 10: continue        # last frame!
        if pins == 10 and roll == 1:
            frame += 1
            score += balls[i+1]
            score += balls[i+2]
            prev, roll = 0, 1
        elif prev + pins == 10:
            frame += 1
            score += balls[i+1]
            prev, roll = 0, 1
        elif roll == 1:
            roll, prev = 2, pins
        else:
            frame += 1
            prev, roll = 0, 1
    return score


def test_bowling():
    '''Testing bowling function'''
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 300 == bowling([10] * 12)
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert 190 == bowling([9,1] * 10 + [9])
    sheet = [9, 1, 0, 10, 10, 10, 6, 2, 7, 3, 8, 2, 10, 9, 0, 9, 1, 10]
    assert 168 == bowling(sheet)

test_bowling()

# sheet = [9, 1, 0, 10, 10, 10, 6, 2, 7, 3, 8, 2, 10, 9, 0, 9, 1, 10]
# print bowling(sheet, verbose=False)

'''

1   [9  1] 
2   [0  10]  
3   [10]  
4   [10]  
5   [6  2]  

     82 points total after fifth frame

6   [7  3]
7   [8  2]  
8   [10]  
9   [9  0]  

     158 points after ninth frame

10  [9  1  10]

     178 points with final frame

------------------------------------

10      9 + 1 + 0
20      0 + 10 + 10
26      10 + 10 + 6
18      10 + 6 + 2
 8      6 + 2

18      7 + 3 + 8
20      8 + 2 + 10

19      10 + 9 + 0
 9      9 + 0

20      9 + 1 + 10

------------------------------------

82 + 38 + 28 + 20

'''
