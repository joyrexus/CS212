import re

def compile_word(word):
    """
    Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'

    """
    if word.isupper():
        terms = ["{0}*{1}".format(10**i, l) for (i,l) in enumerate(word[::-1])]
        return "(" + '+'.join(terms) + ")"
    else:
        return word


# Modify the function compile_formula so that the function 
# it returns, f, does not allow numbers where the first digit
# is zero. So if the formula contained YOU, f would return 
# False anytime that Y was 0 
def compile_formula(f, verbose=False):
    letters = ''.join(set(re.findall('[A-Z]', f)))
    nonzero = re.findall('([A-Z])[A-Z]', f)
    conds = ['{0} != 0'.format(z) for z in nonzero]
    params = ', '.join(letters)
    tokens =  [compile_word(t) for t in re.split('([A-Z]+)', f)]
    body = ''.join(tokens)
    F = 'lambda {0}: {1}'.format(params, body)
    if verbose: 
        print f
        print F
    return eval(F), letters


compile_formula('YOU == ME**2', verbose=True)
                  
                  

