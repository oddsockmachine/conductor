# Log to a file, good for debugging
import logging
logging.basicConfig(filename='sequencer.log',level=logging.DEBUG)


THEME = "A"
# The ints used to represent the state of leds on an led_grid
LED_BLANK = {"A":0, "B": 0,}[THEME]
LED_CURSOR = {"A":1, "B": 2,}[THEME]
LED_ACTIVE = {"A":2, "B": 3,}[THEME]
LED_SELECT = {"A":3, "B": 3,}[THEME]
LED_BEAT = {"A":1, "B": 1,}[THEME]
LED_SCALE_PRIMARY = {"A":9, "B": 9,}[THEME]
LED_SCALE_SECONDARY = {"A":9, "B": 9,}[THEME]

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
colors  =[RED, ORANGE,YELLOW, GREEN,CYAN,BLUE,INDIGO,PURPLE]

# The ints used to represent the state of notes on a note_grid
NOTE_OFF = 0
NOTE_ON = 3

# The glyphs used to display cell information/states in the CLI
DISPLAY = {0: '. ', 1:'░░', 2:'▒▒', 3:'▓▓'}
PALLETE = {0:(1,1,1), 1:(8,3,0), 2:(18,7,0), 3:(18,7,1)}

W = 8  # Width of the display grid
H = 8  # Width of the display grid

# Maximum number of instruments - limited by 16 available midi channels,
# but we may want to run 2 separate sequencers with 8 channels in future
MAX_INSTRUMENTS = 16
