"""Project-wide constants."""

from pathlib import Path

from traiter.terms.csv_ import Csv

# Location of files and directories
BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('brazil') > -1 else Path.cwd().parent
DATA_DIR = BASE_DIR / 'data'
BRAZIL_DIR = DATA_DIR / 'brazil'
BRAZIL_FAMILIES = BRAZIL_DIR / 'families.json'

# Rule steps
GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
LINK_STEP = 'link'

# Character lists and regexes used in rules
CLOSE = ' ) ] '.split()
COLON = ' : '.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = '– - –– --'.split()
DOT = ' . '.split()
INT = r'^\d+$'
INT_RE = r'\d+'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()

PARTS = ['part', 'subpart']

# Terms and dicts made from them
TERM_PATH = BASE_DIR / 'brazil' / 'vocabulary' / 'terms.csv'
TERMS = Csv.read_csv(TERM_PATH)
TERMS += Csv.hyphenate_terms(TERMS)

REPLACE = TERMS.pattern_dicts('replace')
CATEGORY = TERMS.pattern_dicts('category')

# Handle presence or absence clauses with these terms.
PRESENCE = {
    'present': True,
    'presence': True,
    'absent': False,
    'absence': False,
}
PRESENT = list(PRESENCE)

# Abbreviations stopping sentence splitting
ABBREVS = """Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ca """

# Unit conversions
CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
    'centimeters': 10.0,
    'decimeters': 100.0,
    'meters': 1000.0,
    'millimeters': 1.0,
}
