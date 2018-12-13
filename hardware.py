from constants import *
from note_conversion import SCALES
print("Importing hardware connections")
from board import SCL, SDA, D13, D6
import busio
import digitalio
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
        # self.command_cb = command_cb
        button_cb = self.make_cb()
        print("Initializing Trellis")
        for y in range(h):
            for x in range(w):
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
                self.trellis.set_callback(x, y, button_cb)
        self.seq_button = digitalio.DigitalInOut(D13)
        self.ins_button = digitalio.DigitalInOut(D6)
        print("Done")
        return

    def get_cmds(self):
        self.trellis.sync()
        return {'cmd': None}


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
        if self.ins_button.value:
            self.draw_ins_menu(status)
        elif self.seq_button.value:
            self.draw_seq_menu(status)
        else:
            for x in range(len(led_grid)):
                for y in range(len(led_grid[x])):
                    col = PALLETE[led_grid[x][y]]
                    self.led_matrix[x][y] = col
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

    def draw_seq_menu(self, status):
        # Remember to blank all cells
        # menu for sequencer: instrument num on right column, pages on left, repeats pointing right
        # #O##  #
        # ##    #
        # ###   O
        # ###   #
        page_stats = status['page_stats']
        for i in range(status['ins_total']):
            self.led_matrix[self.grid_w-1][i] = RED
        self.led_matrix[self.grid_w-1][status['ins_num']] = GREEN
        for i in range(status['page_total']):
            self.led_matrix[0][i] = RED
        for i in range(status['repeat_total']):
            self.led_matrix[i][status['page_num']-1] = YELLOW
        self.led_matrix[status['repeat_total']-1][status['page_num']-1] = GREEN

        return

    def draw_ins_menu(self, status):
        # Menu for instrument settings (key, scale, octave, speed) spelled out
        # Remember to blank all cells
        for x in range(len(self.led_matrix)):
            for y in range(len(self.led_matrix[x])):
                self.led_matrix[x][y] = OFF
        # Speed:
        speed = len(status['division'])
        for i in range(5):
            self.led_matrix[i][0] = RED
        for i in range(speed):
            self.led_matrix[i][0] = GREEN
        # Scale:  # TODO may have to wrap around to second line
        scale = status['scale']
        scales = list(SCALES.keys())
        scale_i = scales.index(scale)
        for i in range(len(scales)):
            self.led_matrix[i][1] = BLUE
        self.led_matrix[scale_i][1] = CYAN
        # Key
        key = status['key']
        sharp = "#" in key
        key = key.replace('#','')
        letter = LETTERS[key]
        for r, row in enumerate(letter):
            for c, col in enumerate(row):
                if letter[r][c] == 1:
                    self.led_matrix[c][3+r] = INDIGO
        if sharp:
            self.led_matrix[4][3] = INDIGO
            self.led_matrix[4][4] = INDIGO
        # Octave:
        octave = int(status['octave'])
        print(octave)
        for i in range(7):
            print(self.grid_w, i)
            self.led_matrix[7][self.grid_w-1-i] = ORANGE
        self.led_matrix[7][self.grid_w-1-octave] = RED


        # >>>>
        # ____#___
        #
        # ###    X
        # #      O
        # ### #  X
        # #   ## X
        # ### ## X



        return

    def make_cb(self):
        def button_cb(xcoord, ycoord, edge):
            if edge == NeoTrellis.EDGE_RISING:
                if not self.seq_button.value: # Normal mode
                    self.command_cb({'cmd': 'note', 'x': xcoord, 'y': ycoord})
                else: # Menu mode - look up location of press and return cmd
                    {'cmd': None}
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
