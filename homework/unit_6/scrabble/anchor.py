def prefixes(word):
    '''
    Return a list of the initial sequences of a word, not 
    including the complete word.

    '''
    return [word[:i] for i in range(len(word))]

def init(wordfile):
    '''
    Read the words from a file and return set of words 
    and set of prefixes (based on words).
    
    '''
    words = set(open(wordfile).read().split())
    return words, set(p for w in words for p in prefixes(w))

WORDS, PREFIXES = init('words4k.txt')

class anchor(set):
    '''
    An anchor is where a new word can be placed and has a set of
    allowable letters.

    '''

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ANY = anchor(LETTERS)   # unconstrained anchor

def remove(hand, letters):
    '''
    Return a new hand where one instance of letter from letters
    is removed from hand (if present).

    '''
    for l in letters:
        hand = hand.replace(l, '', 1)
    return hand

def find_prefixes(hand, prefix='', maxsize=None, results=None):
    '''
    Find prefixes (of words) that can be made from letters in hand.
    
    '''
    if results is None: results = set()
    if prefix in WORDS or prefix in PREFIXES: results.add(prefix)
    if prefix in PREFIXES:
        for l in hand:
            find_prefixes(remove(hand,l), prefix+l, maxsize, results)
    return results

def add_suffixes(hand, prefix, start, row, results, anchored=True):
    '''
    Add all possible suffixes and accumulate (start, word) pairs
    in results.

    '''
    i = start + len(prefix)
    if prefix in WORDS and anchored and not is_letter(row[i]):
        results.add((start, prefix))
    if prefix in PREFIXES:
        square = row[i]
        if is_letter(square):
            add_suffixes(hand, prefix+square, start, row, results)
        elif is_empty(square):
            valid = square if is_anchor(square) else ANY
            for l in hand:
                if l in valid:
                    hand = remove(l, hand)
                    # hand = hand.replace(l, '', 1)
                    add_suffixes(hand, prefix+l, start, row, results)
    return results

def row_plays(hand, row):
    '''
    Return a set of legal plays in row given hand.

    A row play is a (start, 'WORD') pair, where `start` is an
    index in the row for which we can play the word 'WORD'.

    '''
    results = set()
    args = (row, results, False)
    # for each permissible prefix, add all suffixes, keeping words
    for i, square in enumerate(row[1:-1], 1):
        if is_anchor(square):
            prefix, max = legal_prefix(i, row)
            if prefix:      # add to the letters already on board
                start = i - len(prefix)
                add_suffixes(hand, prefix, start, *args)
            else:           # empty to left so find all possible prefixes
                for prefix in find_prefixes(hand, maxsize=max):
                    start = i - len(prefix)         # starting index
                    hand = remove(hand, prefix)     # remove prefix letters
                    add_suffixes(hand, prefix, start, *args)
    return results

def legal_prefix(i, row):
    '''
    A legal prefix of an anchor at row[i] is either a string of letters
    already on the board, or new letters that fit into an empty space.

    Return a (prefix, max) pair for anchor at index i in row.

    `max` is the maximum size of the possible prefix for the anchor.

    `prefix` is the empty string if the square(s) adjacent to
    the anchor are empty. Otherwise it consists of the adjacent
    letters.

    For example, for the row below we return ('BE', 2) for the anchor 
    at row[9] and ("", 2) for the anchor at row[6].

    | A x y . . . B E . C . . . D . |
      1 2 3 4 5 6 7 8 9

    '''
    s = i
    prefix, max = '', 0
    while is_letter(row[s-1]): s -= 1
    if s < i:
        prefix, max = ''.join(row[s:i]), i - s
    else:
        while is_empty(row[s-1]) and not is_anchor(row[s-1]): s -= 1
        prefix, max = '', i - s
    return prefix, max

def is_anchor(square): return isinstance(square, anchor)

def is_empty(square): return is_anchor(square) or square in ('.', '*')

def is_letter(square): return isinstance(square, str) and square in LETTERS


if __name__ == '__main__':

    assert 'I' in ANY
    assert isinstance(ANY, set)
    assert isinstance(ANY, anchor)
    assert isinstance(anchor(), set)
    assert not isinstance(anchor, set)
    assert not isinstance(LETTERS, set)

    '''
    Consider the anchors `x` and `y` in the diagram below.

    When using these anchors to form a word in their row, they are 
    constrained by the "cross" letters beneath them.

    Thus, we use a constrained set of letters to represent the anchor,
    viz., the set of letters that could be used to form a word in
    their respective column.

    So, for the `y` anchor, we're constrained to use the letters 
    "M", "O", "A", or "B" because these are the only letters that
    could form two letter words found in our dictionary of permissible
    words, viz.: "my", "oy", "ay", or "by".

    '''
    #   1 2 3 4 5 6 7 8 9    12    15    # indices of each square
    # | J . . . . . . . . . . . . . . |
    # | A x y . . . B E . C . . . D . |  # row to consider
    # | G U Y . . . . . . . . . . . . |
    x, y = anchor('MNX'), anchor('MOAB')

    #       0   1  2 3  4   5  6    7   8  9
    row = ['|', 'A', x, y, '.', '.', ANY, 
           'B', 'E', ANY, 'C', ANY, '.', ANY, 'D', ANY, '|']
    hand = 'ABCEHKN'

    print row_plays(hand, row)

    assert legal_prefix(2, row) == ('A', 1)
    assert legal_prefix(3, row) == ('', 0)
    assert legal_prefix(6, row) == ('', 2)
    assert legal_prefix(9, row) == ('BE', 2)
    assert legal_prefix(11, row) == ('C', 1)
    assert legal_prefix(13, row) == ('', 1)

    assert is_empty('.')
    assert is_empty(ANY)
    assert is_empty(anchor('ABC'))
    assert is_empty(x)

    assert not is_empty('L')
    assert not is_empty('|')

    assert is_anchor(x)
    assert is_anchor(y)
    assert is_anchor(anchor('X'))


