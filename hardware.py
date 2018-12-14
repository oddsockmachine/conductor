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
        trelli = [[NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x31)],
                  [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30)],]
        self.trellis = MultiTrellis(trelli)
        self.grid_h = h
        self.grid_w = w
        self.led_matrix = [[(0,0,0) for x  in range(w)] for y in range(h)]
        self.old_led_matrix = [[(0,0,0) for x  in range(w)] for y in range(h)]
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
        if self.ins_button.value:
            self.draw_ins_menu(status)
        elif self.seq_button.value:
            self.draw_seq_menu(status)
        else:
            self.draw_note_grid(led_grid)
        self.redraw_diff()
        return

    def blank_screen(self):
        for x in range(len(self.led_matrix)):
            for y in range(len(self.led_matrix[x])):
                self.led_matrix[x][y] = OFF

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

    def draw_note_grid(self, led_grid):
        for x in range(len(led_grid)):
            for y in range(len(led_grid[x])):
                col = PALLETE[led_grid[x][y]]
                self.led_matrix[x][y] = col
        return

    def draw_seq_menu(self, status):
        # menu for sequencer: instrument num on right column, pages on left, repeats pointing right
        # #O##  #
        # ##    #
        # ###   O
        # ###   #
        self.blank_screen()

#  'ins_num': 1,
#  'ins_total': 16,
#  'page_num': 1,
#  'page_stats': [1],
#  'page_total': 1,
#  'repeat_num': 1,
#  'repeat_total': 1,
        # Draw instrument selector
        for i in range(status['ins_total']):
            self.led_matrix[self.grid_w-1][i] = RED
        self.led_matrix[self.grid_w-1][status['ins_num']-1] = GREEN
        # Draw page/repeats info
        page_stats = status['page_stats']
        page_num = status['page_num']
        repeat_total = status['repeat_total']
        repeat_num = status['repeat_num']
        for i, page_reps in enumerate(page_stats):
            for rep in range(page_reps):
                self.led_matrix[rep][i] = RED
        for i in range(repeat_total):
            self.led_matrix[i][page_num-1] = YELLOW
        self.led_matrix[repeat_num-1][page_num-1] = GREEN
        # self.led_matrix[status['repeat_total']-1][status['page_num']-1] = GREEN

        return

    def draw_ins_menu(self, status):
        # Menu for instrument settings (key, scale, octave, speed) spelled out
                # >>>>
                # ____#___
                #
                # ### #  X
                # #   #  O
                # ### #  X
                # #      X
                # ###    X
        self.blank_screen()
        # Speed:
        speed = status['division']
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
        for i in range(7):
            self.led_matrix[7][self.grid_w-1-i] = ORANGE
        self.led_matrix[7][self.grid_w-1-octave] = RED
        return

    def make_cb(self):
        def button_cb(xcoord, ycoord, edge):
            if edge == NeoTrellis.EDGE_RISING:
                if self.ins_button.value:  # Button from instrument menu
                    if xcoord == 7:  # Octave
                        self.command_cb({'cmd':'change_octave', 'octave': self.grid_w-1-ycoord})
                    if ycoord == 0 and xcoord <= 4:  # Divison/speed
                        self.command_cb({'cmd':'change_division', 'div': xcoord})
                    if ycoord == 1 and xcoord <= 1:  # Scale
                        self.command_cb({'cmd':'cycle_scale', 'dir': {0:-1,1:1}[xcoord]})
                    if ycoord == 7 and xcoord == 0:  # key
                        self.command_cb({'cmd':'cycle_key', 'dir': -1})
                    if ycoord == 3 and xcoord == 0:  # key
                        self.command_cb({'cmd':'cycle_key', 'dir': 1})

                elif self.seq_button.value: # Normal mode
                    # Button from sequencer menu
                    self.command_cb({'cmd': None})
                else: # Menu mode - look up location of press and return cmd
                    self.command_cb({'cmd': 'note', 'x': xcoord, 'y': self.grid_w-1-ycoord})
            return
        return button_cb
