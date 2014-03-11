******
README
******

This directory contains code for an algorithm that makes an optimal move 
in a scrabble game.  This is primarily Norvig's code from Unit 6 of his CS212
course.

We're going to use Norvig's code as a basis for our own scrabble playing
algorithm and web-based scrabble game.  That is, we're going to construct 
a scrabble game where you can play against another online opponent or against
our scrabble playing bot, hubot.


Concept Inventory
=================

Norvig's CS212 course is largely problem driven.  Norvig presents us with a
problem and shows us how to break down the problem into component pieces. We
solve the problem by implementing the solution, bit by bit, a piece at a time.
The first step in this process is to create a concept inventory, a list of the
items implicit in the problem statement that are likely to factor into the
solution.  Alongside each concept, we list a possible implementation strategy:
how we might represent the concept programmatically. The inventory and our
initial representations may prove to be insufficient.  We may have overlooked a
critical concept necessary to represent the overall problem.  Or we may find
our component representations too unwieldy or inefficient as we begin to piece
them together into a larger whole.  But an initial inventory gives a handle on
the problem.  We can revise it as we proceed, refining it as we gain more
insight into the problem domain and its subtler aspects.

Below is Norvig's initial inventory and proposed representations.

* board - 2D array

* blank - str (an empty string)

* letters - str
  * words - str
  * hand - str

* play - tuple of (position, direction, word)

* legal play - boolean function taking a play

* score - function calculating score
  * letters - dict indicating letter values
  * play - fn
  * bonus - mapping from position to score multiplier

* dictionary - set(words)
