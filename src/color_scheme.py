# Inputs:
#     brightness: how bright the whole device appears (should be set in global settings)
#     color-scheme: 2-color gradient for background, plus a pallette of colors for each sprite (set globally)
#     sprite: which pixel to render, eg background, root note, falling droplet, beatline, active, cursor
# Load available schemes in from json/yaml data

# hardware.display.draw_all>draw_note_grid takes a grid of sprites
# These are dereferenced from constants.pallette to give a grid of (r,g,b)
# At the call to `col = c.PALLETE[led_grid[x][y]]`, we could instead call
# col = color.get_color(sprite, x, y)
# Where sprite is the type of pixel (background, active, etc), and x/y may be
# used for gradient effects

from glob import glob
from yaml import load
from colour import Color
# https://pypi.org/project/colour/0.1.1/


# Some constants, used like atoms/enums
BLANK = 'BLANK'
CURSOR = 'CURSOR'
ACTIVE = 'ACTIVE'
SELECT = 'SELECT'
BEAT = 'BEAT'
SCALE_PRIMARY = 'SCALE_PRIMARY'
SCALE_SECONDARY = 'SCALE_SECONDARY'
DROPLET_MOVING = 'DROPLET_MOVING'
DROPLET_SPLASH = 'DROPLET_SPLASH'
DROPLET_STOPPED = 'DROPLET_STOPPED'
DRUM_OFF = 'DRUM_OFF'
DRUM_SELECT = 'DRUM_SELECT'
DRUM_ACTIVE = 'DRUM_ACTIVE'
DRUM_CHANGED = 'DRUM_CHANGED'


class ColorScheme(object):
    """docstring for ColorScheme."""

    def __init__(self, yaml_data):
        super(ColorScheme, self).__init__()
        self.brightness = 0.1
        self.gradient_from = (0, 0, 0)
        self.gradient_to = (0, 0, 0)
        self.gradient = []
        self.pallette = {
            'BLANK': (0, 0, 0),
            'CURSOR': (0, 0, 0),
            'ACTIVE': (0, 0, 0),
            'SELECT': (0, 0, 0),
            'BEAT': (0, 0, 0),
            'SCALE_PRIMARY': (0, 0, 0),
            'SCALE_SECONDARY': (0, 0, 0),
            'DROPLET_MOVING': (0, 0, 0),
            'DROPLET_SPLASH': (0, 0, 0),
            'DROPLET_STOPPED': (0, 0, 0),
            'DRUM_OFF': (0, 0, 0),
            'DRUM_SELECT': (0, 0, 0),
            'DRUM_ACTIVE': (0, 0, 0),
            'DRUM_CHANGED': (0, 0, 0),
        }
        self.import_yaml(yaml_data)
        self.gradient = self.gradient_1d(self.gradient_from, self.gradient_to, 32)

    def import_yaml(self, yaml):
        self.brightness = yaml['brightness']
        self.gradient_from = Color(yaml['gradient']['from'])
        self.gradient_to = Color(yaml['gradient']['to'])
        print(yaml['pallette'])
        for p in self.pallette.keys():
            print(p)
            self.pallette[p] = yaml['pallette'][p]
        self
        return

    def get_color(self, sprite, x=None, y=None):
        # Lookup sprite RGB, calculate based on x/y if necessary
        if sprite == BLANK:
            col = self.gradient[x+y]
        else:
            col = self.pallette[sprite]
        return col

    def col_to_rgb(self, col):
        rgb = col.get_rgb()
        return (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))

    def gradient_1d(self, start, stop, steps):
        gradient = list(map(self.col_to_rgb, start.range_to(stop, steps)))
        return gradient


SCHEMES = {}


def load_schemes():
    """Load in all named schemes from saved data"""
    files = glob('./src/color_schemes/*.yml')
    for y_path in files:
        with open(y_path, 'r') as y_file:
            y_scheme = load(y_file)
        new_scheme = ColorScheme(y_scheme)
        SCHEMES[y_scheme['name']] = new_scheme
    return


load_schemes()

from pprint import pprint
pprint(SCHEMES)
pprint(SCHEMES['default'].gradient)


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
# colors  = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, PURPLE]
PALLETE = {0: (1, 1, 1), 1: (3, 2, 0), 2: (18, 7, 0), 3: (18, 7, 1)}


class Colors(object):
    """docstring for Colors."""

    def __init__(self, arg):
        super(Colors, self).__init__()
        self.arg = arg
        self.brightness = 0.5
        self.theme = "A"

        OFF = (0, 0, 0)
        RED = (255, 0, 0)
        ORANGE = (255, 125, 125)
        YELLOW = (255, 150, 0)
        GREEN = (0, 255, 0)
        CYAN = (0, 255, 255)
        BLUE = (0, 0, 255)
        INDIGO = (180, 0, 255)
        PURPLE = (255, 0, 255)
        colors = {"OFF": OFF,
                  "RED": RED,
                  "ORANGE": ORANGE,
                  "YELLOW": YELLOW,
                  "GREEN": GREEN,
                  "CYAN": CYAN,
                  "BLUE": BLUE,
                  "INDIGO": INDIGO,
                  "PURPLE": PURPLE}

        self.scheme = []
        self.lookup = [colors]

    def get(self):
        return

    def set_brightness(self, brightness):
        if 1 < brightness or brightness < 0:
            return
        self.brightness = float(brightness)
        return
