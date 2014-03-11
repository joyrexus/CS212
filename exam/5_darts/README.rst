*****
Darts
*****

This problem deals with probability in the game of darts.


Overview
========

In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  

Each section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. 

.. image:: http://goo.gl/i7XJ9


Rings
-----

S = single
D = double
T = trible


Sections
--------

1 to 20 and B (bullseye, worth 25 points)


Targets
-------

Targets are the ring/section intersections on a dart board.

* S20 = 20 
* D20 = 40
* T20 = 60

::

    assert points('S20') == ring('S') * section('20')
    assert points('DB') == ring('D') * section('B')


1. Doubling Out
===============

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].

::

    assert double_out(170) == ['T20', 'T20', 'DB']
    #                 170  ==    60   + 60  + 50
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB','DB'])
    #                 100  is    (60  +  40) or (50 + 50)


A strategy for ``double_out``
-----------------------------

I decided to choose the result that has the highest valued target(s) 
first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. 

At first I thought I would need three passes: first try to solve with 
one dart, then with two, then with three.  But I realized that if we 
include 0 as a possible dart value, and always try the 0 first, then 
we get the effect of having three passes, but we only have to code one 
pass.  

So I created ``ordered_points`` as a list of all possible scores that a 
single dart can achieve, with 0 first, and then descending::

    [0, 60, 57, ..., 1].  
    
I iterate dart1 and dart2 over that; then dart3 must be whatever is left 
over to add up to total.  If dart3 is a valid element of points, then we 
have a solution.  

But the solution, is a list of numbers, like ``[0, 60, 40]``; we need to 
transform that into a list of target names, like ``['T20', 'D20']``.

We do that by defining name(d) to get the name of a target that scores d.  
When there are several choices, we must choose a double for the last dart, 
but for the others I prefer the easiest targets first: 'S' is easiest, 
then 'T', then 'D'.


2. Modeling Accuracy
====================

It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?

We describe the model below.


Ring Accuracy
-------------

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Here's the general breakdown::

    if ring == 'T': 
        ('S', miss)
        ('T', 1 - miss)

    if ring == 'D':
        ('S', miss * .5)
        ('OFF', miss * .5)
        ('D', 1 - miss)

    if ring == 'S':
        miss *= .2
        ('D', miss * .5)
        ('T', miss * .5)
        ('S', 1 - miss)

    if ring == 'SB':
        ('S', miss * .75)
        ('DB', miss * .25)
        ('SB', 1 - miss)

    if ring == 'DB':
        miss *= 3
        ('S', miss * (2/3))
        ('SB', miss * (1/3))
        ('DB', 1 - miss)


Section Accuracy
----------------

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is::

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.


Clarifications
==============

Let me try to clarify a bit more. Some people in the discussion forum were confused about the miss ratio -- they didn't get the idea that there are two independent ways to miss, by ring and by section. One way to implement that is to have separate functions to return probability distributions for ring and section outcomes. For example, consider aiming for the S20 target with a miss ratio of 0.2. The S ring is the thick one, so the miss ratio is reduced to 1/5 * 0.2, and we have::

    >>> ring_outcome('S20', .2)
    {'S': 0.96, 'D': 0.02, 'T': 0.02}

    >>> section_outcome('S20', .2)
    {'1': 0.1, '5': 0.1, '20': 0.8}

    >>> outcome('S20', .2)
    {'D20': 0.016, 'S1': 0.096, 'T5': 0.002, 'S5': 0.096, 
     'T1': 0.002, 'S20': 0.768, 'T20': 0.016, 'D5': 0.002, 'D1': 0.002}

Most of the discussion questions center (ha ha) on the bulls-eye. According to the definition, we have::

    >>> ring_outcome('SB', .2)
    {'SB': 0.8, 'S': 0.15, 'DB': 0.05}

    >>> section_outcome('SB', .2)
    {'B': 0.8, '11': 0.01, '10': 0.01, '13': 0.01, '20': 0.01, 
     '14': 0.01, '17': 0.01, '16': 0.01, '19': 0.01, '18': 0.01, 
     '1': 0.01, '3': 0.01, '2': 0.01, '5': 0.01, '4': 0.01, '7': 0.01, 
     '6': 0.01, '9': 0.01, '15': 0.01, '12': 0.01, '8': 0.01}

First make sure that you can duplicate these results (whether you explicitly have separate ring_outcome and section_outcome function, or whether you have the calculations combined into one function).

For most people, the confusion comes in combining these, in particular, what happens when the section outcome says 'B' but the ring outcome says 'S'? We decided that the grading program will be lenient: it allows the interpretation that these outcomes combine to 'SB' or the interpretation that it is evenly split among all sectors in the 'S' ring: S1, S2, ... S20. So we have either::

    >>> outcome('SB', .2)
    {'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04, 
     'S6': 0.01, 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01, 
     'S12': 0.01, 'S11': 0.01, 'S10': 0.01, 'S17': 0.01, 'S16': 0.01, 'S15': 0.01, 
     'S14': 0.01, 'S7': 0.01, 'S20': 0.01, 'SB': 0.76}

or::

    >>> outcome('SB', .2)
    {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016, 'DB': 0.04, 
    'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016, 'S19': 0.016, 'S18': 0.016, 
    'S13': 0.016, 'S12': 0.016, 'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 
    'S15': 0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64}

(I prefer the second answer, but we messed up the description in the first version of the question, so we are allowing both answers.)

Finally, for those who are interested in learning more, consider this page: http://www.stat.cmu.edu/~ryantibs/darts/

Note that the simplified target model I present in this exercise duplicates some of the findings they come up with, particularly in the path of the optimal target as the miss ratio increases.
