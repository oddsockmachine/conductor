from constants import *
print("Importing hardware connections")
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
print("Done")

class Display(object):
    """docstring for Display."""
    def __init__(self, w=W, h=H, command_cb=None):
        super(Display, self).__init__()
        print("Creating i2c bus")
        i2c_bus = busio.I2C(SCL, SDA)
        print("Done")
        trelli = [
            [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x31)],
            [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30)]
            ]
        self.trellis = MultiTrellis(trelli)

        self.grid_h = h
        self.grid_w = w
        self.led_matrix = [[(0,0,0) for x  in range(w)] for y in range(h)]
        self.old_led_matrix = [[(0,0,0) for x  in range(w)] for y in range(h)]
        self.button = None
        # self.command_cb = command_cb
        button_cb = self.make_cb()
        print("Initializing Trellis")
        for y in range(h):
            for x in range(w):
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
                self.trellis.set_callback(x, y, button_cb)
        print("Done")
        return

    def get_cmds(self):
        self.trellis.sync()
        """Check serial in port for messages. If commands come in, delegate calls to relevant components"""
        if self.button:
            x,  y = self.button
            self.button = None
            return {'cmd': 'note', 'x': x, 'y': y}

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

        #TODO updating whole grid over i2c takes time, use python to diff screen status, then write out to hardware

        for x in range(len(led_grid)):
            for y in range(len(led_grid[x])):
                # col = LOW if led_grid[x][y] else OFF
                col = PALLETE[led_grid[x][y]]

                self.led_matrix[x][y] = col
                # self.trellis.color(x, y, col)
        self.redraw_diff()
        return

    def redraw_diff(self):
        diffs = []
        for x in range(len(self.led_matrix)):
            for y in range(len(self.led_matrix[x])):
                if self.led_matrix[x][y] != self.old_led_matrix[x][y]:
                    # diffs.append((x, y, self.led_matrix[x][y]))
                    self.trellis.color(x, y, self.led_matrix[x][y])
                self.old_led_matrix[x][y] = self.led_matrix[x][y]
        # This method might be better once the grid is much bigger
        # for diff in diffs:
        #     self.trellis.color(diff[0],diff[1],diff[2])
        return


    def make_cb(self):
        def button_cb(xcoord, ycoord, edge):
            if edge == NeoTrellis.EDGE_RISING:
                self.command_cb({'cmd': 'note', 'x': xcoord, 'y': ycoord})
            return
            # return {'cmd': None}
            # return {'cmd': 'note', 'x': grid_x, 'y': self.grid_h - grid_y -1}
            # return {'cmd': 'ins', 'ins': ins}
            # return {'cmd': 'add_page'}
            # return {'cmd': 'change_division', 'div': (-1 if (x-self.page_x <=5) else 1)}
            # return {'cmd': 'dec_rep', 'page': y-self.page_y-1}
            # return {'cmd': 'page_down', 'page': y-self.page_y-1}
            # return {'cmd': 'page_up', 'page': y-self.page_y-1}
            # return {'cmd': 'inc_rep', 'page': y-self.page_y-1}

        return button_cb
