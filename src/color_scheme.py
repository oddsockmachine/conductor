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
from yaml import load
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
        self.pallette_lookup = {
            c.LED_BLANK: 'BLANK',
            c.LED_CURSOR: 'CURSOR',
            c.LED_ACTIVE: 'ACTIVE',
            c.LED_SELECT: 'SELECT',
            c.LED_BEAT: 'BEAT',
            c.LED_SCALE_PRIMARY: 'SCALE_PRIMARY',
            c.LED_SCALE_SECONDARY: 'SCALE_SECONDARY',
            c.DROPLET_MOVING: 'DROPLET_MOVING',
            c.DROPLET_SPLASH: 'DROPLET_SPLASH',
            c.DROPLET_STOPPED: 'DROPLET_STOPPED',
            c.DRUM_OFF: 'DRUM_OFF',
            c.DRUM_SELECT: 'DRUM_SELECT',
            c.DRUM_ACTIVE: 'DRUM_ACTIVE',
            c.DRUM_CHANGED: 'DRUM_CHANGED',
        }
        self.import_yaml(yaml_data)
        self.gradient = self.gradient_1d(self.gradient_from, self.gradient_to, 32)

    def import_yaml(self, yaml):
        self.brightness = yaml['brightness']
        self.gradient_from = Color(yaml['gradient']['from'])
        self.gradient_to = Color(yaml['gradient']['to'])
        print(yaml['pallette'])
        for p in self.pallette_lookup.keys():
            print(p)
            self.pallette[p] = yaml['pallette'][self.pallette_lookup[p]]
        self
        return

    def get_color(self, sprite, x=None, y=None):
        # Lookup sprite RGB, calculate based on x/y if necessary
        if sprite == c.LED_BLANK:
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


def load_schemes():
    """Load in all named schemes from saved data"""
    SCHEMES = {}
    files = glob('./src/color_schemes/*.yml')
    for y_path in files:
        with open(y_path, 'r') as y_file:
            y_scheme = load(y_file)
        new_scheme = ColorScheme(y_scheme)
        SCHEMES[y_scheme['name']] = new_scheme
    return SCHEMES
