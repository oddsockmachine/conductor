from constants import *

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

class Display(object):
    """docstring for Display."""
    def __init__(self, w=W, h=H):
        super(Display, self).__init__()
        i2c_bus = busio.I2C(SCL, SDA)
        trelli = [
            [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x31)],
            [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30)]
            ]
        self.trellis = MultiTrellis(trelli)

        self.grid_h = h
        self.grid_w = w
        return

    def get_cmds(self):
        """Check serial in port for messages. If commands come in, delegate calls to relevant components"""
        return {'cmd': None}
        return {'cmd': 'note', 'x': grid_x, 'y': self.grid_h - grid_y -1}
        return {'cmd': 'ins', 'ins': ins}
        return {'cmd': 'add_page'}
        return {'cmd': 'change_division', 'div': (-1 if (x-self.page_x <=5) else 1)}
        return {'cmd': 'dec_rep', 'page': y-self.page_y-1}
        return {'cmd': 'page_down', 'page': y-self.page_y-1}
        return {'cmd': 'page_up', 'page': y-self.page_y-1}
        return {'cmd': 'inc_rep', 'page': y-self.page_y-1}

    def draw_all(self, status, led_grid):

        # pprint(status)
        # {'division': '>>',
        #  'ins_num': 1,
        #  'ins_total': 16,
        #  'isdrum': False,
        #  'key': 'e',
        #  'octave': '2',
        #  'page_num': 1,
        #  'page_stats': [1],
        #  'page_total': 1,
        #  'repeat_num': 1,
        #  'repeat_total': 1,
        #  'scale': 'pentatonic_maj'}
        # pprint(led_grid)
        for x in range(len(led_grid)):
            for y in range(len(led_grid[x])):
                col = color[y] if led_grid[x][y] else OFF
                self.trellis.color(x, y, col)

        return
