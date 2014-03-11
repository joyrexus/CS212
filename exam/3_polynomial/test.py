from main import *


def test_poly():
    '''Testing poly constructor'''
    coefs = (10, 20, 30)
    p = poly(coefs)
    assert p.coefs == coefs
    assert p.__name__ == '30 * x**2 + 20 * x + 10'
    assert same_name(p.__name__, '30 * x**2 + 20 * x + 10')
    assert p(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p(x) == 30 * x**2 + 20 * x + 10

    coefs = (0, 1, 2, 3, 4, 5)
    p = poly(coefs)
    assert p.coefs == coefs
    expected = '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x'
    assert p.__name__ == expected
    assert same_name(p.__name__, expected)
    assert p(1) == 15
    assert p(2) == 258

    coefs = (0, 0, 0, 1) 
    p = poly(coefs)
    assert p.coefs == coefs
    assert p.__name__ == 'x**3'
    assert same_name(p.__name__, 'x**3')
    assert p(1) == 1
    assert p(2) == 8

    coefs = (1, 1)
    p = poly(coefs)
    assert p.coefs == coefs
    assert p.__name__ == 'x + 1'

def test_is_poly():
    '''Testing is_poly function'''
    coefs = (3,2,1)
    p = poly(coefs)
    print p.coefs
    assert is_poly(p)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

def test_add():
    '''Testing add function'''
    a = poly((10, 20, 30))
    b = poly((0, 0, 0, 1))
    c = poly((1, 2, 3))
    assert a.__name__ == '30 * x**2 + 20 * x + 10'
    assert b.__name__ == 'x**3'
    assert c.__name__ == '3 * x**2 + 2 * x + 1'

    p = add(a, b)
    assert is_poly(p)
    assert p.coefs == (10, 20, 30, 1)
    assert p.__name__ == 'x**3 + 30 * x**2 + 20 * x + 10'

    p = add(a, c)
    assert is_poly(p)
    assert p.coefs == (11, 22, 33)
    assert p.__name__ == '33 * x**2 + 22 * x + 11'

def test_subtraction():
    '''Testing sub function'''
    a = poly((10, 20, 30))
    b = poly((1, 2, 3))
    p = sub(a, b)
    assert is_poly(p)
    assert p.coefs == (9, 18, 27)
    assert p.__name__ == '27 * x**2 + 18 * x + 9'

def test_multiply():
    '''Testing mul function'''
    coefs = (0, 0, 0, 1) 
    p = poly(coefs)
    assert p.__name__ == 'x**3'
    assert p(2) == 8

    q = mul(p, p)   # x**3 * x**3  =  x**6
                    #  0  1  2  3  4  5  6
    assert q.coefs == (0, 0, 0, 0, 0, 0, 1)
    assert q.__name__ == 'x**6'
    assert q(2) == 64

    r = mul(p, q)           # x**6 * x**3
    s = mul(p, mul(p, p))   # x**6 * x**3
    assert r(2) == 512 == s(2)

    a = poly((4, 1, 2, 0))    # 4 * x**0 + 1 * x**1 + 2 * x**2
    b = poly((2, 1))          # 2 * x**0 + 1 * x**1
    #
    #                               a  *  b
    # (4 * x**0 + 1 * x**1 + 2 * x**2) * (2 * x**0 + 1 * x**1)
    #
    # [a * (2 * x**0)] + [a * (1 * x**1)]
    #
    # (8 * x**0 + 2 * x**1 + 4 * x**2 +
    #             4 * x**1 + 1 * x**2 + 2 * x**3)
    #
    #  8        + 6 * x    + 5 * x**2 + 2 * x**3
    #
    c = mul(a, b)   # 2 * x**3 + 5 * x**2 + 6 * x + 8
    assert c.coefs == (8, 6, 5, 2, 0)
    assert c.__name__ == '2 * x**3 + 5 * x**2 + 6 * x + 8'

def test_power():
    '''Testing power function'''
    q = poly((1, 1))
    assert q.__name__ == 'x + 1'
    expected = 'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 ' + \
               '+ 210 * x**6 + 252 * x**5 + 210 * x**4 '     + \
               '+ 120 * x**3 + 45 * x**2 + 10 * x + 1'
    assert power(q, 10).__name__ == expected

def test_terms():
    '''Testing terms function'''
    coefs = (10, 20, 30)
    p = poly(coefs)
    assert p.__name__ == '30 * x**2 + 20 * x + 10'
    assert terms(p) == ['30 * x**2', '20 * x', '10']

def test_diff_term():
    '''Testing diff_term function'''
    # The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
    assert diff_term('20').__name__ == ''
    assert diff_term('20 * x').__name__ == '20'
    assert diff_term('x').__name__ == '1'
    assert diff_term('30 * x**2').__name__ == '60 * x'

def test_derivative():
    '''Testing deriv function'''
    # the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).
    coefs = (10, 20, 30)
    p = poly(coefs)
    assert p.__name__ == '30 * x**2 + 20 * x + 10'
    assert p(1) == 60
    d = deriv(p) 
    assert d.__name__ == '60 * x + 20'

    coefs = (0, 1, 2, 3, 4, 5)
    p = poly(coefs)
    assert p.coefs == coefs
    expected = '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x'
    assert p.__name__ == expected
    assert p(1) == 15
    assert p(2) == 258

    d = deriv(p)
    expected = '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1'
    assert d.__name__ == expected
    assert d(1) == 55
    assert d(2) == 573

def test_integrate_term():
    '''Testing integrate_term function'''
    assert integrate_term('60 * x').__name__ == '30 * x**2'
    assert integrate_term('20').__name__ == '20 * x'

def test_integral():
    '''Testing integral function'''
    # integral of '60 * x + 20' should be '30 * x**2 + 20 * x'
    p = poly((20, 60))  # 60 * x + 20
    assert p.__name__ == '60 * x + 20'
    assert integral(p).__name__ == '30 * x**2 + 20 * x'

def test_coefs():
    '''Testing coefs attribute'''
    p, q = poly((10,20,30)), poly((1,2,3))
    assert add(p,q).coefs == (11,22,33)
    assert sub(p,q).coefs == (9,18,27) 
    assert mul(p,q).coefs == (10,40,100,120,90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    expected = (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)
    assert power(poly((1, 1)), 10).coefs == expected
    assert deriv(p).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)

