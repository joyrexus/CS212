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

def find_words(letters, prefix='', words=set()):
    if prefix in WORDS: words.add(prefix)
    if prefix in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), prefix+L, words)
    return words


if __name__ == '__main__':

    assert len(WORDS)    == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES

