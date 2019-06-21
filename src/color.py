# Inputs:
#     brightness: how bright the whole device appears (should be set in global settings)
#     color-scheme: 2-color gradient for background, plus a pallette of colors for each sprite (set globally)
#     sprite: which pixel to render, eg background, root note, falling droplet, beatline, active, cursor
# Load available schemes in from json/yaml data

from dataclasses import dataclass

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


@dataclass
class Color:
    r: int
    g: int
    b: int


class ColorScheme(object):
    """docstring for ColorScheme."""

    def __init__(self):
        super(ColorScheme, self).__init__()
        self.brightness = 0.1
        self.gradient = ((0, 0, 0), (0, 0, 0))
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

    def get_sprite_color(self, sprite):
        # Lookup sprite RGB
        return

    def get_background_color(self, x, y):
        # Calculate background pixel form gradient
        return


SCHEMES = {}


def load_schemes():
    """Load in all named schemes from saved data"""
    return


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
