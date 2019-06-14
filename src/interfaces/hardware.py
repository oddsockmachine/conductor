import constants as c
from board import SCL, SDA, D13, D6
import busio
import digitalio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
from time import sleep
from interfaces.lcd import lcd
print("Imported hardware connections")

AUTO_WRITE = False


class Display(object):
    """docstring for Display."""

    def __init__(self, w=c.W, h=c.H, command_cb=None):
        super(Display, self).__init__()
        print("Creating i2c bus")
        lcd.flash("Creating i2c bus")
        i2c_bus = busio.I2C(SCL, SDA)
        lcd.setup_hw(i2c_bus)
        print("i2c bus created")
        lcd.flash("i2c bus created")
        print("Creating Trelli")
        lcd.flash("Creating Trelli")
        trelli = [[], [], [], []]
        addrs = [[0x2e, 0x2f, 0x30, 0x31],
                 [0x32, 0x33, 0x34, 0x35],
                 [0x36, 0x37, 0x38, 0x39],
                 [0x3a, 0x3b, 0x3c, 0x3d]]
        # Create trelli sequentially with a slight pause between each
        for x, slice in enumerate(addrs):
            for y, addr in enumerate(slice):
                t = NeoTrellis(i2c_bus, False, addr=addr)
                t.pixels.auto_write = False
                trelli[x].append(t)
                sleep(0.2)
        print("Linking Trelli")
        lcd.flash("Linking Trelli")
        self.trellis = MultiTrellis(trelli)

        print("Trelli linked")
        lcd.flash("Trelli linked")
        self.grid_h = h
        self.grid_w = w
        self.led_matrix = [[(0, 0, 0) for x in range(w)] for y in range(h)]
        self.old_led_matrix = [[(0, 0, 0) for x in range(w)] for y in range(h)]
        button_cb = self.make_cb()
        print("Initializing Trelli inputs")
        lcd.flash("Initializing Trelli inputs")
        for y in range(h):
            for x in range(w):
                sleep(0.01)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
                sleep(0.01)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
                self.trellis.set_callback(x, y, button_cb)
        self.seq_button = digitalio.DigitalInOut(D13)
        self.ins_button = digitalio.DigitalInOut(D6)
        print("Inputs initialized")
        lcd.flash("Inputs initialized")
        return

    def get_cmds(self):
        try:
            self.trellis.sync()  # TODO undo? Fails if called too often
        except Exception as e:
            print("HW error: {}".format(str(e)))
        m = {'cmd': None}
        if self.ins_button.value:
            m['cmd'] = "CONFIG_A"
        elif self.seq_button.value:
            m['cmd'] = "CONFIG_B"
        return m

    def draw_all(self, status, led_grid):
        # if self.ins_button.value:
        #     self.draw_ins_menu(status)
        # elif self.seq_button.value:
        #     self.draw_seq_menu(status)
        # else:
        self.draw_note_grid(led_grid)
        self.redraw_diff()
        return

    def blank_screen(self):
        for x in range(len(self.led_matrix)):
            for y in range(len(self.led_matrix[x])):
                self.led_matrix[x][y] = c.OFF

    def redraw_diff(self):
        diffs = []
        for x in range(len(self.led_matrix)):
            for y in range(len(self.led_matrix[x])):
                if self.led_matrix[x][y] != self.old_led_matrix[x][y]:
                    diffs.append((x, y, self.led_matrix[x][y]))
                    # self.trellis.color(x, y, self.led_matrix[x][y])
                self.old_led_matrix[x][y] = self.led_matrix[x][y]
        # This method might be better once the grid is much bigger
        # t_start = perf_counter()
        for diff in diffs:
            self.trellis.color(diff[0], diff[1], diff[2])
            sleep(0.001)
        if len(diffs) > 0:
            if not AUTO_WRITE:
                for ts in self.trellis._trelli:
                    for t in ts:
                        t.pixels.show()
        # t_stop = perf_counter()
        # logger.info(str(t1_stop-t1_start))
        return

    def draw_note_grid(self, led_grid):
        for x in range(len(led_grid)):
            for y in range(len(led_grid[x])):
                col = c.PALLETE[led_grid[x][y]]
                self.led_matrix[x][self.grid_h-1-y] = col
        return

    def make_cb(self):
        def button_cb(xcoord, ycoord, edge):
            if edge == NeoTrellis.EDGE_RISING:
                if self.ins_button.value:  # Button from instrument menu
                    if xcoord == 7:  # Octave
                        self.command_cb({'cmd': 'change_octave', 'octave': self.grid_w-1-ycoord})
                    if ycoord == 0 and xcoord <= 4:  # Divison/speed
                        self.command_cb({'cmd': 'change_division', 'div': xcoord})
                    if ycoord == 1 and xcoord <= 1:  # Scale
                        self.command_cb({'cmd': 'cycle_scale', 'dir': {0: -1, 1: 1}[xcoord]})
                    if ycoord == 7 and xcoord == 0:  # key
                        self.command_cb({'cmd': 'cycle_key', 'dir': -1})
                    if ycoord == 3 and xcoord == 0:  # key
                        self.command_cb({'cmd': 'cycle_key', 'dir': 1})
                    if ycoord == 0 and xcoord == 7:  # key
                        self.command_cb({'cmd': 'random_rpt'})

                elif self.seq_button.value:  # Normal mode
                    # Button from sequencer menu
                    self.command_cb({'cmd': None})
                else:  # Menu mode - look up location of press and return cmd
                    self.command_cb({'cmd': 'note', 'x': xcoord, 'y': self.grid_h-1-ycoord})
            return
        return button_cb

    def draw_load_screen(self):
        return
