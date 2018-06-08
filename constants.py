# Log to a file, good for debugging
import logging
logging.basicConfig(filename='sequencer.log',level=logging.DEBUG)

# The ints used to represent the state of leds on an led_grid
LED_BLANK = 0
LED_SELECT = 1
LED_CURSOR = 2
LED_ACTIVE = 3

# The ints used to represent the state of notes on a note_grid
NOTE_OFF = 0
NOTE_ON = 3

# The glyphs used to display cell information/states in the CLI
DISPLAY = {0: '. ', 1:'░░', 2:'▒▒', 3:'▓▓'}

W = 20  # Width of the display grid
H = 20  # Width of the display grid

# Maximum number of instruments - limited by 16 available midi channels,
# but we may want to run 2 separate sequencers with 8 channels in future
MAX_INSTRUMENTS = 16
