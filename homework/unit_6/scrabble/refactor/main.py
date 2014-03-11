WORDS, PREFIXES = None, None

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, 
              M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, 
              X=8, Y=4, Z=10, _=0)


class Letters(list):
    '''
    Experimental class for our hand/letters representation.

    '''
    def omit(self, letters):
        for l in letters: self.remove(l)
        return self


class Anchor(set):
    '''
    An anchor is a space on the board where a new word can be placed.

    Every anchor has a set of allowable letters that can be used
    in its space to make a word.

    '''


class Square(set):
    '''
    Representation of a square on the game board.

    '''
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, x):
        self.string = x
        if len(x) == 1:
            self.is_letter = x in self.LETTERS
            self.is_anchor = x == '_'
            self.is_border = x == '|'
            self.is_empty  = x in ('.', '_', '*')
            self.points = POINTS[x] if self.is_letter else 0
            if self.is_anchor: x = self.LETTERS
        else:
            self.is_letter = False
            self.is_anchor = True
            self.is_border = False
            self.is_empty  = True
            self.points = 0
        self = super(Square, self).__init__(x)

    def __eq__(self, y):
        if isinstance(y, str) and self.is_letter:
            return y == self.string
        return super(Square, self).__eq__(y)

    def __str__(self):
        return self.string


class Row(list):
    '''
    Represent a row on a scrabble board.

    indices:       0 1 2 3 4 5 6 7 8 9 . . . . . . 16
    >>> row = Row('| A * * . . _ B E _ C _ . _ D _ |')

    '''
    def __init__(self, squares):
        squares = [Square(s) for s in squares.split()]
        self = super(Row, self).__init__(squares)

    def __repr__(self):
        return ' '.join(str(s) for s in self)

    def enumerate(self):
        '''
        Yield (index, square) for each square in row, 
        omitting borders.

        '''
        for i, square in enumerate(self[1:-1], 1):
            yield (i, square)

    def legal_prefix(self, i):
        '''
        A legal prefix of an anchor at square i is either a string
        of letters already on the board or new letters that fit into
        an empty space -- in both cases, these letters are/should
        immediately precede the anchor location at square i.
        
        We return the tuple (prefix, max) to indicate
        this, where `max` is the maximum size the legal prefix can
        be, viz., the length of the prefix on the board (if it exists)
        or the number of empty spaces in which a prefix could be placed.

        indices:       0 1 2 3 4 5 6 7 8 9 . . . . . . 16
        >>> row = Row('| A * * . . _ B E _ C _ . _ D _ |')
        >>> row.legal_prefix(6)
        ('', 2)
        >>> row.legal_prefix(9)
        ('BE', 2)

        '''
        s = i   # will change to be the starting index of the prefix
        prefix, max = '', 0
        if self[s-1].is_letter:
            while self[s-1].is_letter: s -= 1   # extend prefix backward
            prefix = ''.join(str(x) for x in self[s:i])
            max = i - s                         # length of prefix
        else:
            while self[s-1].is_empty and not self[s-1].is_anchor: s -= 1
            prefix = ''                         # no pre-existing prefix
            max = i - s                         # length of empty spaces
        return prefix, max

    def add_suffixes(self, hand, prefix, start, results, anchored=True):
        '''
        Add all possible suffixes, and accumulate (start, word) pairs 
        in results.

        '''
        i = start + len(prefix)
        square = self[i]
        if prefix in WORDS and anchored and not square.is_letter:
            results.add((start, prefix))
        if prefix in PREFIXES:       
            if square.is_letter:
                self.add_suffixes(hand, prefix+square, start, results)
            elif square.is_empty:
                squares = square if square.is_anchor else Square('_')
                for L in hand:
                    if L in squares:
                        self.add_suffixes(hand.replace(L, '', 1), 
                                          prefix+L, start, results)
        return results

    def plays(self, hand):
        '''
        Return a set of legal plays within row. 

        A row play is a (start, word) pair, where `start` is 
        the row index (square) in which `word` can be played.

        For each allowable prefix, we add all suffixes, keeping words.

        '''
        results = set()
        prefix, max = '', 0
        args = (self, results, False)
        for i, _ in self.enumerate():
            if _.is_anchor:
                prefix, max = self.legal_prefix(i)
                if prefix:  # add to letters already on board
                    start = i - len(prefix)
                    add_suffixes(hand, prefix, start, *args)
            else:       # empty to left, check all possible prefixes
                for prefix in find_prefixes(hand):
                    if len(prefix) <= max:
                        start = i - len(prefix)
                        hand = omitfrom(hand, prefix)
                        add_suffixes(hand, prefix, start, *args)
        return results


_ = ANY = Anchor(LETTERS)   # anchor that can be any letter

def omitfrom(hand, letters):
    for l in letters:
        hand = hand.replace(l, '', 1)
    return hand

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

WORDS, PREFIXES = init('../words4k.txt')

def defaults(func):
    '''
    Decorator that injects and initializes the `prefix` and 
    `results` keyword args into the args passed to `func` if 
    not already present in the function call.

    '''
    def wrapper(*args, **kwargs):
        if len(args) < 2 and 'prefix' not in kwargs:
            kwargs['prefix'] = ''
        if len(args) < 3 and 'results' not in kwargs:
            return func(*args, results=set(), **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper

@defaults
def find_words(hand, prefix, results):
    '''Find all words derivable from the letters in our hand.'''
    if prefix in WORDS: results.add(prefix)
    if prefix in PREFIXES:
        for L in hand:
            find_words(omitfrom(hand, L), prefix+L, results)
    return results

def find_prefixes(hand, prefix='', results=None):
    '''Find all prefixes derivable from the letters in our hand.'''
    if results is None: results = set([])
    if prefix in PREFIXES:
        results.add(prefix)
        for L in hand: 
            find_prefixes(omitfrom(hand, L), prefix+L, results)
    return results

def word_score(word):
    '''
    Return the score for word, which is just the sum of the
    individual letter points.

    '''
    return sum(POINTS[c] for c in word)

def word_plays(hand, letters, sort_by=word_score, n=10):
    '''
    Find all possible word plays that can be made from hand 
    given one of the letters in `letters`.

    '''
    results = set()
    for prefix in find_prefixes(hand):
        for L in letters:
            add_suffixes_orig(omitfrom(hand, prefix), prefix+L, results)
    if sort_by:
        return sorted(results, reverse=True, key=sort_by)[:n]
    else:
        return list(results)[:n]

@defaults
def add_suffixes_orig(hand, prefix, results):
    '''
    Return the set of words that can be formed by extending
    prefix with letters in hand.

    '''
    if prefix in WORDS: results.add(prefix)
    if prefix in PREFIXES:
        for L in hand:
            add_suffixes_orig(omitfrom(hand, L), prefix+L, results)
    return results

def add_suffixes(hand, pre, start, row, results, anchored=True):
    '''
    Add all possible suffixes, and accumulate (start, word) pairs 
    in results.

    '''
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre in PREFIXES:       
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, Anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), 
                                 pre+L, start, row, results)
    return results

def row_plays(hand, row):
    '''
    Return a set of legal plays in row. 

    A row play is a (start, word) pair, where `start` is 
    the index in the row in which `word` can be played.

    For each allowable prefix, we add all suffixes, keeping words.

    '''
    results = set()
    prefix, max = '', 0
    args = (row, results, False)
    # for i, _ in row.enumerate():
    for i, _ in enumerate(row[1:-1], 1):
        if isinstance(_, Anchor):
            # prefix, max = row.prefix_status(i)
            prefix, max = legal_prefix(i, row)
            if prefix:  # add to letters already on board
                start = i - len(prefix)
                add_suffixes(hand, prefix, start, *args)
        else:       # empty to left, check all possible prefixes
            for prefix in find_prefixes(hand):
                if len(prefix) <= max:
                    start = i - len(prefix)
                    hand = omitfrom(hand, prefix)
                    add_suffixes(hand, prefix, start, *args)
    return results

def legal_prefix(i, row):
    '''
    A legal prefix of an anchor at square i is either a string
    of letters already on the board or new letters that fit into
    an empty space -- in both cases, these letters are/should
    immediately precede the anchor location at square i.
    
    We return the tuple (prefix, max) to indicate
    this, where `max` is the maximum size the legal prefix can
    be, viz., the length of the prefix on the board (if it exists)
    or the number of empty spaces in which a prefix could be placed.

    indices:       0 1 2 3 4 5 6 7 8 9 . . . . . . 16
    >>> row = Row('| A * * . . _ B E _ C _ . _ D _ |')
    >>> legal_prefix(6, row)
    ('', 2)
    >>> legal_prefix(9, row)
    ('BE', 2)

    '''
    s = i   # will change to be the starting index of the prefix
    prefix, max = '', 0
    if is_letter(row[i-1]):
        while is_letter(row[s-1]): s-= 1    # extend range of prefix backward
        prefix = ''.join(row[s:i])          # letters found from s to i
        max = i - s                         # length of prefix
    else:
        while is_empty(row[s-1]) and not isinstance(row[s-1], Anchor): s -= 1
        prefix = ''                         # no pre-existing prefix
        max = i - s                         # length of empty spaces
    return prefix, max

def is_letter(x):
    return isinstance(x, str) and x in LETTERS

def is_empty(x):
    return x == '.' or x == '*' or isinstance(x, Anchor)


if __name__ == '__main__':

    hand = Letters('LETTERS')
    assert hand == list('LETTERS')
    assert hand.omit('LET') == list('TERS')
    assert hand.omit('ST') == list('ER')

    expected = ['WOS', 'SOW', 'SOD', 'ODS', 'DOS', 'ORS', 'SO', 'OS']
    assert word_plays('WORD', 'S', n=5) == expected[:5]

    assert len(ANY) == 26
    assert 'I' in ANY
    assert 'Q' in ANY

    x = Anchor('MNX')
    y = Anchor('ABMO')
    assert 'N' in x
    assert 'N' not in y

    row = Row('| A MNX . . . _ B E _ C _ . _ D _ |')
    for i, _ in row.enumerate():
        assert _ == row[i]

    assert is_letter('Z')
    assert is_empty('.')
    assert is_empty(Anchor('XYZ'))

    s = Square('Z')
    assert s.is_letter
    assert not s.is_anchor
    assert not s.is_empty

    s = Square('XYZ')
    assert not s.is_letter
    assert s.is_anchor
    assert s.is_empty

    row = Row('| A MNX MOAB . . _ B E _ C _ . _ D _ |')
    assert row.legal_prefix(1) == ('', 0)
    assert row.legal_prefix(2) == ('A', 1)
    assert row.legal_prefix(6) == ('', 2)
    assert row.legal_prefix(9) == ('BE', 2)

    hand = Letters('ABCEHKN')
    expected = set([(4,'NA'), (4,'EH'), (4,'AH'), (4,'EN'), (7,'BE'), 
                    (4,'BA'), (4,'AN'), (4,'AE'), (4,'HA'), (1,'AN'), 
                    (4,'NE'), (1,'ANA'), (4,'AB'), (4,'KA'), (4,'HE'), 
                    (4,'BE'), (7,'BENCH')])
    # print row.plays(hand)

    # norvig's version

    MNX = Anchor('MNX')
    MOAB = Anchor('MOAB')
    a_row = ['|', 'A', MNX, MOAB, '.', '.', ANY, 'B', 'E', ANY, 'C', 
             ANY, '.', ANY, 'D', ANY, '|']
    a_hand = 'ABCEHKN'
    assert row_plays(a_hand, a_row) == expected

