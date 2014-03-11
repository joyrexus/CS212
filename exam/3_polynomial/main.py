import re
from itertools import izip_longest
from collections import defaultdict


def poly(coefs):
    '''
    Return a function that represents the polynomial with 
    given coefficients.

    For example, if coefs=(10, 20, 30), return the function of x 
    that computes `30 * x**2 + 20 * x + 10`.  
    
    Also store the coefs on the .coefs attribute of the function, 
    and the str of the formula on the .__name__ attribute.
    
    '''
    terms = ['{0} * x**{1}'.format(c, e) 
                for e, c in enumerate(coefs) if c != 0]
    terms.reverse()
    expr = ' + '.join(terms)
    def p(x):
        return eval(expr)
    p.coefs = coefs
    p.__name__ = simplify(expr)
    return p

x_to_first = re.compile(r'x\*\*1\b')
x_to_zero = re.compile(r'x\*\*0\b')
float_zero = re.compile(r'\.0\b')

def simplify(expr):
    '''Simplify polynomial expression string.'''
    expr = expr.lstrip('1 * ')
    expr = expr.replace(' 1 * ', ' ')
    expr = expr.replace(' * x**0', '')
    expr = expr.replace(' + x**0', ' + 1')
    expr = x_to_first.sub('x', expr)
    expr = x_to_zero.sub('1', expr)
    expr = float_zero.sub('', expr)
    expr.strip()
    return expr

def same_name(a, b):
    '''
    Use to check equivalence of polynomial name attributes.

    Allows for some variation in polynomial expression formatting.
    
    '''
    normalized = lambda x: x.replace(' ', '').replace('+-', '-')
    return normalized(a) == normalized(b)

is_poly = lambda x: hasattr(x, 'coefs')

zip = lambda x, y: izip_longest(x, y, fillvalue=0)

def add(a, b):
    'Return a new poly that is the sum of polynomials a and b.'
    coefs = tuple(x + y for x, y in zip(a.coefs, b.coefs))
    return poly(coefs)

def sub(a, b):
    'Return a new poly that is the difference of polynomials a and b.'
    coefs = tuple(x - y for x, y in zip(a.coefs, b.coefs))
    return poly(coefs)

def mul(a, b):
    '''
    Return a new poly that is the product of polynomials a and b.

    '''
    coefs = defaultdict(int)
    for i, x in enumerate(a.coefs):
        for j, y in enumerate(b.coefs):
            k = i + j           # add indices/powers 
            coefs[k] += x * y   # multiply coefficients

    coefs = tuple(coefs.get(i, 0) for i in range(max(coefs.keys())+1))
    return poly(coefs)

def power(p, n):
    '''
    Return a new polynomial which is `p` to the n-th power.

    `n` should be a non-negative integer.

    '''
    if n < 2: 
        return p
    else:
        return mul(p, power(p, n-1))

def terms(p):
    '''
    Return tuple of terms in polynomial p.

    >>> coefs = (10, 20, 30)
    >>> p = poly(coefs)
    >>> p.__name__ == '30 * x**2 + 20 * x + 10'
    True
    >>> terms(p)
    ['30 * x**2', '20 * x', '10']

    '''
    return p.__name__.split(' + ')

def deriv(p):
    '''
    Return the derivative of a function p (with respect to its argument).

    The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).

    The derivative of a sum is the sum of the derivatives.

    So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20):

    >>> coefs = (10, 20, 30)
    >>> p = poly(coefs)
    >>> p.__name__ == '30 * x**2 + 20 * x + 10'
    True
    >>> p(1) == 60
    True
    >>> d = deriv(p) 
    >>> d.__name__ == '60 * x + 20'
    True

    '''
    d = poly((0,))
    for t in terms(p):
        d = add(d, diff_term(t))
    return d


# pattern for single polynomial term
term_pt = re.compile(r'(?P<coef>\d+)?(?:\s?x\*\*(?P<expo>\d+))?$')
coef_pt = re.compile(r'(?P<coef>\d+)')
expo_pt = re.compile(r'x\*\*(?P<expo>\d+)$')
x_pt = re.compile(r'x$')

def diff_term(term):
    '''
    Differentiate a polynomial term.

    The deriviative of `c * x**n` is `c*n * x**(n-1)`.

    '''
    term = x_pt.sub('x**1', term)   # "x" => "x**1"
    c, n = 1, 0
    m = coef_pt.match(term)
    if m: 
        c = int(m.group('coef'))
    m = expo_pt.search(term)
    if m: 
        n = int(m.group('expo'))
    if c*n == 0: return poly((0,))
    power = [0] * (n - 1)
    coefs = power + [c*n]           # c*n * x**(n-1)
    t = poly(coefs)
    return t

def integral(p, b=0):
    '''
    Return the integral (anti-derivative) of a function p 
    (with respect to its argument).

    The integral of a polynomial term `c*n * x**(n-1)` is `c * x**n`

    So, the integral of '60 * x + 20' should be '30 * x**2 + 20 * x'

    Takes a constant `b` as an optional argument.  Any value of b 
    is an equally good anti-derivative.

    >>> p = poly(60, 20)
    >>> p.__name__ == '60 * x + 20'
    True
    >>> i = integral(p)                     # for any constant b.
    >>> i.__name__ == '30 * x**2 + 20 * x'
    True
    >>> i = integral(p, b=2)                # for any constant b.
    >>> i.__name__ == '30 * x**2 + 20 * x + 2'
    True

    '''
    i = poly((0,))
    for t in terms(p):
        i = add(i, integrate_term(t, b))
    return i


def integrate_term(term, b=0):
    '''
    Integrate a polynomial term.

    The deriviative of `c * x**n` is `c*n * x**(n-1)`.

    So, the integral of `c*n * x**(n-1)` is `c * x**n`
                     ...      `c * x**n` is `c/n * x**(n+1)`

    '''
    term = x_pt.sub('x**1', term)   #  x  => x**1
    if term.isdigit():              # 20  =>  20 * x**0
        term += ' * x**0'
    c, n = 1, 0
    m = coef_pt.match(term)
    if m: 
        c = int(m.group('coef'))
    m = expo_pt.search(term)
    if m: 
        n = int(m.group('expo'))
    power = [0] * (n + 1)
    coefs = power + [c/(n + 1.0)]   # c/n * x**(n+1)
    t = poly(coefs)
    return t


if __name__ == '__main__':

    # integral of '60 * x + 20' should be '30 * x**2 + 20 * x'
    p = poly((20, 60))
    assert p.__name__ == '60 * x + 20'
    q = poly((0, 20, 30))
    assert q.__name__ == '30 * x**2 + 20 * x'
    assert integral(p).__name__ == q.__name__ \
                                == '30 * x**2 + 20 * x'

    #  5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + 1 * x**1 + 0 * x**0
    #  5          4          3          2          1          0
    coefficients = range(6)  # poly will represent coefs in reverse order
    p = poly(coefficients)
    assert p.__name__ == '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x'
    assert p(1) == 15
    assert p(2) == 258

    p = poly((3,2,1))
    assert p.__name__ == 'x**2 + 2 * x + 3'
    assert p(1) == 6
