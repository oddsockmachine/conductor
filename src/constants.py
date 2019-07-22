# coding=utf-8

# Log to a file, good for debugging
import logging
logging.basicConfig(filename='sequencer.log', level=logging.DEBUG)

save_location = './saved/'
save_extension = '.json'

# The ints used to represent the state of leds on an led_grid
LED_BLANK = 0  # TODO rename to seq_
LED_CURSOR = 1
LED_ACTIVE = 2
LED_SELECT = 3
LED_BEAT = 4
LED_SCALE_PRIMARY = 5
LED_SCALE_SECONDARY = 6
LED_EDIT = 4
DROPLET_MOVING = 7
DROPLET_SPLASH = 8
DROPLET_STOPPED = 9
DROPLET_HEIGHT = 10

DRUM_OFF = 11
DRUM_SELECT = 12
DRUM_ACTIVE = 13
DRUM_CHANGED = 14

SLIDER_TOP = 20
SLIDER_BODY = 21

INSTRUMENT_A = 90
INSTRUMENT_B = 91
INSTRUMENT_C = 92
INSTRUMENT_D = 93

KEY_BLACK = 80
KEY_WHITE = 81
KEY_ROOT = 82
KEY_SCALE = 83


# The ints used to represent the state of notes on a note_grid
NOTE_OFF = 0
NOTE_ON = 3

pallette_lookup = {
    LED_BLANK: 'BLANK',
    LED_CURSOR: 'CURSOR',
    LED_ACTIVE: 'ACTIVE',
    LED_SELECT: 'SELECT',
    LED_BEAT: 'BEAT',
    LED_SCALE_PRIMARY: 'SCALE_PRIMARY',
    LED_SCALE_SECONDARY: 'SCALE_SECONDARY',
    DROPLET_MOVING: 'DROPLET_MOVING',
    DROPLET_SPLASH: 'DROPLET_SPLASH',
    DROPLET_STOPPED: 'DROPLET_STOPPED',
    DRUM_OFF: 'DRUM_OFF',
    DRUM_SELECT: 'DRUM_SELECT',
    DRUM_ACTIVE: 'DRUM_ACTIVE',
    DRUM_CHANGED: 'DRUM_CHANGED',
    SLIDER_TOP: 'SLIDER_TOP',
    SLIDER_BODY: 'SLIDER_BODY',
    INSTRUMENT_A: 'INSTRUMENT_A',
    INSTRUMENT_B: 'INSTRUMENT_B',
    INSTRUMENT_C: 'INSTRUMENT_C',
    INSTRUMENT_D: 'INSTRUMENT_D',
}

# The glyphs used to display cell information/states in the CLI
# DISPLAY = {0: '. ', 1:'  ', 2:'OO', 3:'XX'}
DISPLAY = {0: '. ',
           1: '░░',
           2: '▒▒',
           3: '▓▓',
           4: '▒▒',
           7: '░░',
           9: '▒▒',
           8: '▓▓',
           21: '▒▒',
           20: '▓▓',
           80: '░░',
           81: '░░',
           82: '▒▒',
           83: '▓▓',
           90: 'xx',
           91: 'XX',
           92: '//',
           93: r'\\',
           }

W = 16  # Width of the display grid
H = 16  # Width of the display grid

# Maximum number of instruments - limited by 16 available midi channels,
# but we may want to run 2 separate sequencers with 8 channels in future
MAX_INSTRUMENTS = 16

# Note letters
A = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
]
B = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]
C = [
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
]
D = [
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]
E = [
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 0],
    [1, 1, 1],
]
F = [
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 0],
    [1, 0, 0],
]
G = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
]
h = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
]
I = [
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
]
L = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
]
M = [
    [1, 0, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
]
O = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
]
P = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
]
R = [
    [1, 1, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 0, 1],
    [1, 0, 1],
]
S = [
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
]
X = [
    [1, 0, 1],
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
    [1, 0, 1],
]
Y = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
]
PLUS = [
    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
    [0, 0, 0],
]
MINUS = [
    [0, 0, 0],
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0],
]
SHARP = [
    [0, 0, 0],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [0, 0, 0],
]
SPACE = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

ROW = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ]]
COLUMN = [[INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
          [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
          [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
          [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D], ]
INSTRUMENTS = [[INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
               [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
               [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D],
               [INSTRUMENT_A], [INSTRUMENT_B], [INSTRUMENT_C], [INSTRUMENT_D], ]
NUM_INSTRUMENTS = {
    0: INSTRUMENTS[:0],
    1: INSTRUMENTS[:1],
    2: INSTRUMENTS[:2],
    3: INSTRUMENTS[:3],
    4: INSTRUMENTS[:4],
    5: INSTRUMENTS[:5],
    6: INSTRUMENTS[:6],
    7: INSTRUMENTS[:7],
    8: INSTRUMENTS[:8],
    9: INSTRUMENTS[:9],
    10: INSTRUMENTS[:10],
    11: INSTRUMENTS[:11],
    12: INSTRUMENTS[:12],
    13: INSTRUMENTS[:13],
    14: INSTRUMENTS[:14],
    15: INSTRUMENTS[:15],
    16: INSTRUMENTS[:16],
}

SCALE_CHARS = {
    'ionian':     'io',
    'dorian':     'do',
    'phrygian':   'ph',
    'lydian':     'ly',
    'mixolydian': 'mx',
    'aeolian':    'ae',
    'locrian':    'lo',
    'major':      'ma',
    'minor':      'mi',
    'pentatonic_maj':  'p+',
    'pentatonic_min':  'p-',
    'chromatic':  'ch',
}

LETTERS = {'a': A, 'b': B, 'c': C, 'd': D, 'e': E, 'f': F, 'g': G, 'h': h, 'i': I, 'l': L, 'm': M,
           'o': O, 'p': P, 'r': R, 's': S, 'x': X, 'y': Y,
           '+': PLUS, '-': MINUS, '#': SHARP, ' ':  SPACE, 'num_instruments': INSTRUMENTS}
