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

import constants as c
from glob import glob
from yaml import safe_load
from colour import Color
# https://pypi.org/project/colour/0.1.1/


class ColorScheme(object):
    """docstring for ColorScheme."""

    def __init__(self, yaml_data):
        super(ColorScheme, self).__init__()
        self.brightness = 0.1  # TODO user control of brightness
        self.gradient_from = (0, 0, 0)
        self.gradient_to = (0, 0, 0)
        self.gradient = []
        self.pallette = {}
        self.import_yaml(yaml_data)
        self.gradient = self.gradient_1d(self.gradient_from, self.gradient_to, 32)

    def import_yaml(self, yaml):
        self.brightness = yaml['brightness']
        self.gradient_from = Color(yaml['gradient']['from'])
        self.gradient_to = Color(yaml['gradient']['to'])
        c.debug(yaml['pallette'])
        for p in c.pallette_lookup.keys():
            c.debug(p)
            self.pallette[p] = yaml['pallette'][c.pallette_lookup[p]]
        self
        return

    def get_color(self, sprite, x=None, y=None):
        # Lookup sprite RGB, calculate based on x/y if necessary
        if sprite == c.LED_BLANK:
            col = self.gradient[int(x+y/2)]
        else:
            col = self.pallette[sprite]
        return col

    def col_to_rgb(self, col):
        rgb = col.get_rgb()
        return (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))

    def gradient_1d(self, start, stop, steps):
        gradient = list(map(self.col_to_rgb, start.range_to(stop, steps)))
        return gradient


def load_schemes():
    """Load in all named schemes from saved data"""
    SCHEMES = {}
    files = glob('./src/color_schemes/*.yml')
    for y_path in files:
        with open(y_path, 'r') as y_file:
            y_scheme = safe_load(y_file)
        new_scheme = ColorScheme(y_scheme)
        SCHEMES[y_scheme['name']] = new_scheme
    return SCHEMES


SCHEMES = load_schemes()
CURR_SCHEME_NAME = ""


def select_scheme(name):
    CURR_SCHEME_NAME = name
    c.logging.info("selected scheme: {}".format(CURR_SCHEME_NAME))
    return SCHEMES[name]


def next_scheme():
    names = SCHEMES.keys()
    # global CURR_SCHEME_NAME
    i = names.index(CURR_SCHEME_NAME)
    new_i = (i+1) % len(SCHEMES.keys())
    new_name = SCHEMES.keys()[new_i]
    CURR_SCHEME_NAME = new_name
    new_scheme = SCHEMES[CURR_SCHEME_NAME]
    return new_scheme
