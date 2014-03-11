from main import *
from util.profile import Timer

# regression test
hands = dict(
    ABECEDR=set(
    ['BE', 'CARE', 'BAR', 'BA', 'ACE', 'READ', 'CAR', 'DE', 'BED', 'BEE',
        'ERE', 'BAD', 'ERA', 'REC', 'DEAR', 'CAB', 'DEB', 'DEE', 'RED', 'CAD',
        'CEE', 'DAB', 'REE', 'RE', 'RACE', 'EAR', 'AB', 'AE', 'AD', 'ED', 
        'RAD', 'BEAR', 'AR', 'REB', 'ER', 'ARB', 'ARC', 'ARE', 'BRA']
    ),
    AEINRST=set(
    ['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'TIE', 'SIN', 'TAR', 'TAS',
        'RAN', 'SIT', 'SAE', 'RIN', 'TAE', 'RAT', 'RAS', 'TAN', 'RIA', 'RISE',
        'ANESTRI', 'RATINES', 'NEAR', 'REI', 'NIT', 'NASTIER', 'SEAT', 'RATE',
        'RETAINS', 'STAINER', 'TRAIN', 'STIR', 'EN', 'STAIR', 'ENS', 'RAIN', 
        'ET', 'STAIN', 'ES', 'ER', 'ANE', 'ANI', 'INS', 'ANT', 'SENT', 'TEA', 
        'ATE', 'RAISE', 'RES', 'RET', 'ETA', 'NET', 'ARTS', 'SET', 'SER', 
        'TEN', 'RE', 'NA', 'NE', 'SEA', 'SEN', 'EAST', 'SEI', 'SRI', 
        'RETSINA', 'EARN', 'SI', 'SAT', 'ITS', 'ERS', 'AIT', 'AIS', 'AIR', 
        'AIN', 'ERA', 'ERN', 'STEARIN', 'TEAR', 'RETINAS', 'TI', 'EAR', 
        'EAT', 'TA', 'AE', 'AI', 'IS', 'IT', 'REST', 'AN', 'AS', 'AR', 'AT', 
        'IN', 'IRE', 'ARS', 'ART', 'ARE']
    ),
    DRAMITC=set(
    ['DIM', 'AIT', 'MID', 'AIR', 'AIM', 'CAM', 'ACT', 'DIT', 'AID', 'MIR',
        'TIC', 'AMI', 'RAD', 'TAR', 'DAM', 'RAM', 'TAD', 'RAT', 'RIM', 'TI',
        'TAM', 'RID', 'CAD', 'RIA', 'AD', 'AI', 'AM', 'IT', 'AR', 'AT', 'ART',
        'CAT', 'ID', 'MAR', 'MA', 'MAT', 'MI', 'CAR', 'MAC', 'ARC', 'MAD', 
        'TA', 'ARM']
    ),
    ADEINRST=set(
    ['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'DEAR', 'TIE', 'SIN', 'RAD', 
        'TAR', 'TAS', 'RAN', 'SIT', 'SAE', 'SAD', 'TAD', 'RE', 'RAT', 'RAS', 
        'RID', 'RIA', 'ENDS', 'RISE', 'IDEA', 'ANESTRI', 'IRE', 'RATINES', 
        'SEND', 'NEAR', 'REI', 'DETRAIN', 'DINE', 'ASIDE', 'SEAT', 'RATE', 
        'STAND', 'DEN', 'TRIED', 'RETAINS', 'RIDE', 'STAINER', 'TRAIN', 'STIR', 
        'EN', 'END', 'STAIR', 'ED', 'ENS', 'RAIN', 'ET', 'STAIN', 'ES', 'ER',
        'AND', 'ANE', 'SAID', 'ANI', 'INS', 'ANT', 'IDEAS', 'NIT', 'TEA', 
        'ATE', 'RAISE', 'READ', 'RES', 'IDS', 'RET', 'ETA', 'INSTEAD', 'NET', 
        'RED', 'RIN', 'ARTS', 'SET', 'SER', 'TEN', 'TAE', 'NA', 'TED', 'NE',
        'TRADE', 'SEA', 'AIT', 'SEN', 'EAST', 'SEI', 'RAISED', 'SENT', 'ADS', 
        'SRI', 'NASTIER', 'RETSINA', 'TAN', 'EARN', 'SI', 'SAT', 'ITS', 'DIN', 
        'ERS', 'DIE', 'DE', 'AIS', 'AIR', 'DATE', 'AIN', 'ERA', 'SIDE', 'DIT',
        'AID', 'ERN', 'STEARIN', 'DIS', 'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 
        'TA', 'AE', 'AD', 'AI', 'IS', 'IT', 'REST', 'AN', 'AS', 'AR', 'AT', 
        'IN', 'ID', 'ARS', 'ART', 'ANTIRED', 'ARE', 'TRAINED', 'RANDIEST', 
        'STRAINED', 'DETRAINS']
    ),
    ETAOIN=set(
    ['ATE', 'NAE', 'AIT', 'EON', 'TIN', 'OAT', 'TON', 'TIE', 'NET', 'TOE',
        'ANT', 'TEN', 'TAE', 'TEA', 'AIN', 'NE', 'ONE', 'TO', 'TI', 'TAN',
        'TAO', 'EAT', 'TA', 'EN', 'AE', 'ANE', 'AI', 'INTO', 'IT', 'AN', 'AT',
        'IN', 'ET', 'ON', 'OE', 'NO', 'ANI', 'NOTE', 'ETA', 'ION', 'NA', 'NOT',
        'NIT']
    ),
    SHRDLU=set(['URD', 'SH', 'UH', 'US']),
    SHROUDT=set(
    ['DO', 'SHORT', 'TOR', 'HO', 'DOR', 'DOS', 'SOUTH', 'HOURS', 'SOD',
        'HOUR', 'SORT', 'ODS', 'ROD', 'OUD', 'HUT', 'TO', 'SOU', 'SOT', 'OUR',
        'ROT', 'OHS', 'URD', 'HOD', 'SHOT', 'DUO', 'THUS', 'THO', 'UTS', 'HOT',
        'TOD', 'DUST', 'DOT', 'OH', 'UT', 'ORT', 'OD', 'ORS', 'US', 'OR',
        'SHOUT', 'SH', 'SO', 'UH', 'RHO', 'OUT', 'OS', 'UDO', 'RUT']
    ),
    TOXENSI=set(
    ['TO', 'STONE', 'ONES', 'SIT', 'SIX', 'EON', 'TIS', 'TIN', 'XI', 'TON',
        'ONE', 'TIE', 'NET', 'NEXT', 'SIN', 'TOE', 'SOX', 'SET', 'TEN', 'NO',
        'NE', 'SEX', 'ION', 'NOSE', 'TI', 'ONS', 'OSE', 'INTO', 'SEI', 'SOT',
        'EN', 'NIT', 'NIX', 'IS', 'IT', 'ENS', 'EX', 'IN', 'ET', 'ES', 'ON',
        'OES', 'OS', 'OE', 'INS', 'NOTE', 'EXIST', 'SI', 'XIS', 'SO', 'SON',
        'OX', 'NOT', 'SEN', 'ITS', 'SENT', 'NOS']
    )
)

def test_letters():
    '''Testing Letters'''
    hand = Letters('LETTERS')
    assert hand == list('LETTERS')
    assert hand.omit('LET') == list('TERS')
    assert hand.omit('ST') == list('ER')

def test_omitfrom():
    '''Testing omitfrom function'''
    assert omitfrom('LETTERS', 'L') == 'ETTERS'
    assert omitfrom('LETTERS', 'T') == 'LETERS'
    assert omitfrom('LETTERS', 'SET') == 'LTER'

def test_init():
    '''Testing init function'''
    assert len(WORDS)    == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES

def test_find_words():
    '''Testing find_words method'''
    for hand, expected in hands.items():
        result = find_words(hand)
        if result != expected:
            print hand, 'differs from expected:'
            print result ^ expected
        assert result == expected
    timer = Timer()
    t = timer(map, find_words, hands)
    assert t.time < .04

def test_prefixes():
    '''Testing prefixes function'''
    assert prefixes('WORD') == ['', 'W', 'WO', 'WOR']
    assert prefixes('HELLO') == ['', 'H', 'HE', 'HEL', 'HELL']

def test_suffixes():
    '''Testing add_suffixes function'''
    assert add_suffixes_orig('TTER', 'LE') == set(['LET', 'LEE', 'LETTER'])
    assert add_suffixes_orig('ABCEHKN', 'BE') == set(['BE', 'BEE', 'BEN', 
                                                 'BEEN', 'BENCH'])
    expected = set(['NAB', 'BE', 'BEN', 'BA', 'ACE', 'NAE', 'NAH', 
                    'NEB', 'BACK', 'BENCH', 'EN', 'CAN', 'BAN', 'CAB', 
                    'HA', 'BAH', 'HE', 'NA', 'NE', 'AB', 'AE', 'EH', 
                    'KAB', 'AH', 'HAE', 'AN', 'HEN', 'BANK', 'ANE', 
                    'KA', 'NECK', 'KAE', 'KEA', 'EACH', 'KEN'])
    assert add_suffixes_orig('ABCEHKN', '') == expected

def test_word_score():
    '''Testing word_score function'''
    assert word_score('SO') == 2
    assert word_score('SOW') == 6
    assert word_score('DOG') == 5

def test_word_plays():
    '''Testing word_plays function'''
    expected = ['WOS', 'SOW', 'SOD', 'ODS', 'DOS', 'ORS', 'SO', 'OS']
    assert word_plays('WORD', 'S') == expected
    assert word_plays('WORD', 'S', n=5) == expected[:5]

def test_any_letter():
    '''Testing the ANY letter set'''
    assert len(ANY) == 26
    assert 'I' in ANY
    assert 'Q' in ANY

def test_anchor():
    '''Testing the Anchor class'''
    x = Anchor('MNX')
    y = Anchor('ABMO')
    assert 'N' in x
    assert 'N' not in y

def test_square():
    '''Testing Square class'''
    s = Square('Z')
    assert s == 'Z'
    assert s.points == 10
    assert s.is_letter
    assert not s.is_anchor
    assert not s.is_empty
    s = Square('XYZ')
    assert s == set('XYZ')
    assert s.points == 0
    assert not s.is_letter
    assert s.is_anchor
    assert s.is_empty

def test_row():
    '''Testing the Row class'''
    row = Row('| A MNX . . . _ B E _ C _ . _ D _ |')
    assert row[2].is_anchor
    assert 'M' in row[2]
    for i, _ in row.enumerate():
        assert _ == row[i]

def test_add_suffixes():
    '''Testing add_suffixes method of Row'''
    row = Row('| L E . . . . . . . . . . . . . |')
    expected = set([(1,'LET'), (1,'LEE'), (1,'LETTER')])
    assert row.add_suffixes(hand='TTER', prefix='LE',
                            start=1, results=set()) == expected
    '''
    assert add_suffixes('ABCEHKN', 'BE') == set(['BE', 'BEE', 'BEN', 
                                                 'BEEN', 'BENCH'])
    expected = set(['NAB', 'BE', 'BEN', 'BA', 'ACE', 'NAE', 'NAH', 
                    'NEB', 'BACK', 'BENCH', 'EN', 'CAN', 'BAN', 'CAB', 
                    'HA', 'BAH', 'HE', 'NA', 'NE', 'AB', 'AE', 'EH', 
                    'KAB', 'AH', 'HAE', 'AN', 'HEN', 'BANK', 'ANE', 
                    'KA', 'NECK', 'KAE', 'KEA', 'EACH', 'KEN'])
    assert add_suffixes('ABCEHKN', '') == expected
    '''

def test_legal_prefix():
    '''Testing the legal_prefix method of Row'''
    row = Row('| A MNX MOAB . . _ B E _ C _ . _ D _ |')
    assert row.legal_prefix(1) == ('', 0)
    assert row.legal_prefix(2) == ('A', 1)
    assert row.legal_prefix(6) == ('', 2)
    assert row.legal_prefix(9) == ('BE', 2)
    expected = [('',0), ('',0), ('A',1), ('',0), ('',0), ('',1), ('',2), 
                ('',0), ('B',1), ('BE',2), ('',0), ('C',1), ('',0), 
                ('',1), ('',0), ('D',1), ('',0)]
    found = [row.legal_prefix(i) for i in range(len(row))]
    assert found == expected
