# coding=utf-8

# Log to a file, good for debugging
import logging
logging.basicConfig(filename='sequencer.log', level=logging.DEBUG)

save_location = './saved/'
save_extension = '.json'

THEME = "A"
# The ints used to represent the state of leds on an led_grid
LED_BLANK = {"A": 0, "B": 0, }[THEME]
LED_CURSOR = {"A": 1, "B": 2, }[THEME]
LED_ACTIVE = {"A": 2, "B": 3, }[THEME]
LED_SELECT = {"A": 3, "B": 3, }[THEME]
LED_BEAT = {"A": 1, "B": 1, }[THEME]
LED_SCALE_PRIMARY = {"A": 9, "B": 9, }[THEME]
LED_SCALE_SECONDARY = {"A": 9, "B": 9, }[THEME]

DROPLET_MOVING = 2
DROPLET_SPLASH = 3
DROPLET_STOPPED = 1

DRUM_OFF = 0
DRUM_SELECT = 3
DRUM_ACTIVE = 2
DRUM_CHANGED = 1

# TODO calculate and return color tuples based on brightness setting
OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 125, 125)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
INDIGO = (180, 0, 255)
PURPLE = (255, 0, 255)
PURPLE = (10, 0, 10)
LOW = (18, 7, 0)
colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, PURPLE]

# The ints used to represent the state of notes on a note_grid
NOTE_OFF = 0
NOTE_ON = 3

# The glyphs used to display cell information/states in the CLI
# DISPLAY = {0: '. ', 1:'  ', 2:'OO', 3:'XX'}
DISPLAY = {0: '. ', 1: '░░', 2: '▒▒', 3: '▓▓'}
# PALLETE = {0:(1,1,1), 1:(3,2,0), 2:(18,7,0), 3:(18,7,1)}

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
    [1, 1, 1],
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
COLUMN = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], ]
INSTRUMENTS = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], ]
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
