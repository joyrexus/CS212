# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)' 
# Non-uppercase words should remain unchaged.

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

assert compile_word('YOU') == '(1*U+10*O+100*Y)'
assert compile_word('you') == 'you'
