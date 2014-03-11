import random


def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return allmax(hands, key=hand_rank)

def allmax(iter, key=(lambda x: x)):
    "Return a list of all items equal to the max of iter."
    high = max(iter, key=key)
    return [i for i in iter if key(i) == key(high)]

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        a, b = two_pair(ranks)
        return (2, a, b, ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    if ranks == [14, 5, 4, 3, 2]: return range(5, 0, -1)
    return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    hi, lo = ranks[0], ranks[-1]
    return ranks == range(hi, lo-1, -1)

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [suit for rank, suit in hand]
    return len(set(suits)) is 1

def kind(n, ranks):
    """
    Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand.

    """
    for i in ranks:
        if ranks.count(i) is n:
            return i
    return None

def two_pair(ranks):
    """
    If there are two pair, return the two ranks as a tuple: 
    (highest, lowest); otherwise return None.

    """
    pairs = [i for i in set(ranks) if ranks.count(i) is 2]
    return tuple(pairs) if len(pairs) is 2 else None

    
def tests():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "TD TC 8H 7C 7D".split() # Two Pair
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
    assert straight(card_ranks(al)) == True 
    fkranks = card_ranks(fk)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    tpranks = card_ranks(tp)
    assert two_pair(tpranks) == (10, 7)
    sfranks = card_ranks(sf)
    assert two_pair(sfranks) == None
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    return 'tests pass'

def test():
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    return 'tests pass'

cards = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=cards):
    "Return list of numhands lists with n cards each."
    D = deck[:]
    random.shuffle(D)
    return [[D.pop(0) for i in range(n)] for h in range(numhands)]

hand_names = [
    'High Card',
    'Pair',
    '2 Pair',
    '3 Kind',
    'Straight',
    'Flush',
    'Full House',
    '4 Kind',
    'Straight Flush'
    ]

def hand_percentages(n=10*1000):
    counts = [0] * 9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print "%15s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n)



if __name__ == '__main__':
    print deal(3)
    print hand_percentages()
