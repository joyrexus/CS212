import re, string

table = string.maketrans('abc', '123')

exp = 'a + b == c'

leadingzero = re.compile(r'\b0[0-9]') 

def valid(exp):
    '''Evaluate f and return True if valid, False otherwise.'''
    try:
        return not leadingzero.search(exp) and eval(exp.translate(table))
    except:
        return False


assert valid('a + b == c')
assert not valid('a + b == b')
assert not valid('a + b / 0')
assert not valid('0 + b == 012')
