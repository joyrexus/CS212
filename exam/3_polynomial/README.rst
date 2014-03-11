***********
Polynomials
***********

This is the third final exam problem testing our knowledge of functions
and APIs covered in unit 3.


Overview
========

A polynomial is a mathematical formula like::

    (30 * x**2) + (20 * x**1) + (10 * x**0) # explicit form
     30 * x**2  +  20 * x     +  10         # conventional form
     30            20            10         # coefficients
   

More formally, it involves a single variable (here 'x'), and the sum 
of one or more terms, where each term is a real number multiplied by 
the variable raised to a non-negative integer power.

We'll represent a polynomial as a function which computes the formula
when applied to a numeric value x.  We'll define a function named 
``poly`` to construct such polynomial functions given the polynomial's
coeffecients as arguments::

    >>> coefficients = (10, 20, 30)
    >>> p = poly(coefficients)
    >>> p
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>
    >>> p.__name__ 
    '30 * x**2 + 20 * x + 10'
    >>> p.coefs 
    (10, 20, 30)

With the polynomial defined, we can now call it with various values for x::

    >>> p(0)    # 0 + 0 + 10
    10
    >>> p(1)    # 30 + 20 + 10
    60 
    >>> p(2)    # 120 + 40 + 10
    170


Simplifying polynomial function names
-------------------------------------

We're going to store a representation of the constructed
polynomial in the returned function's __name__ attribute.

    >>> coefficients = (10, 20, 30)
    >>> p = poly(coefficients)
    >>> p.__name__ 
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for the name is simplified according
to the following rules:

* Drop terms with zero coefficients ('0 * x**n').

* change '1 * x**n' to 'x**n'.

* change '5 * x**0' to '5'.  

* change 'x**1' to 'x'.

For negative coefficients, like -5, you can use either
'... + -5 * ...' or '... - 5 * ...'.

No spaces around '**' and spaces around '+' and '*' 
are recommended but not required.


Functions
=========

In addition to defining the polynomial constructor *poly*,
you're required to write the following functions:

* is_poly
* add
* sub
* mul
* power
* deriv
* integral

See the tests for examples.

:name: ``poly``
:arguments:  coefs (a tuple of coefficients)
:return:  a function that represents the polynomial with the given coefficients

Usage::

    >>> coefficients = (10, 20, 30)
    >>> p = poly(coefficients)
    >>> p.__name__ 
    '30 * x**2 + 20 * x + 10'
    >>> p.coefs 
    (10, 20, 30)
    >>> p(1)
    60 


Derivatives and Integrals
=========================

If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
    

Extra Credit
============

Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

1. By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

2. Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().

def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
    assert p1(100) == newp1(100) # The new poly objects are still callable.
    assert same_name(p1.__name__,newp1.__name__)
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))

def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert same_name(p1.__name__,newp1.__name__)


