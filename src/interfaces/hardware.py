from constants import debug, W, H, OFF
from config import trellis_addresses
from threading import Thread
from board import SCL, SDA, D13, D6
import busio
import digitalio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
from time import sleep
from interfaces.lcd import lcd
from color_scheme import select_scheme, next_scheme  # TODO add gbl button to cycle scheme
debug("Imported hardware connections")

AUTO_WRITE = False

class Display(Thread):
    """docstring for Display."""

    def __init__(self, button_bus, led_bus, i2c_bus):
        Thread.__init__(self, name='Display')
        # super(Display, self).__init__()
        self.button_bus = button_bus
        self.led_bus = led_bus
        debug("Creating i2c bus")
        lcd.flash("Creating i2c bus")
        # i2c_bus = busio.I2C(SCL, SDA)
        lcd.setup_hw(i2c_bus)
        debug("i2c bus created")
        lcd.flash("i2c bus created")
        debug("Creating Trelli")
        lcd.flash("Creating Trelli")
        trelli = [[], [], [], []]
        # addrs = trellis_addresses
        # Create trelli sequentially with a slight pause between each
        for x, slice in enumerate(trellis_addresses):
            for y, addr in enumerate(slice):
                t = NeoTrellis(i2c_bus, False, addr=addr)
                t.pixels.auto_write = False
                trelli[x].append(t)
                sleep(0.1)
        debug("Linking Trelli")
        lcd.flash("Linking Trelli")
        self.trellis = MultiTrellis(trelli)

        debug("Trelli linked")
        lcd.flash("Trelli linked")
        self.grid_h = H
        self.grid_w = W
        self.state = 'play'
        self.led_matrix = [[(0, 0, 0) for x in range(w)] for y in range(h)]
        self.old_led_matrix = [[(0, 0, 0) for x in range(w)] for y in range(h)]
        button_cb = self.make_cb()
        debug("Initializing Trelli inputs")
        lcd.flash("Initializing Trelli inputs")
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                sleep(0.01)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
                sleep(0.01)
                self.trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
                self.trellis.set_callback(x, y, button_cb)
        self.ins_button = digitalio.DigitalInOut(D13)
        self.gbl_button = digitalio.DigitalInOut(D6)
        debug("Inputs initialized")
        lcd.flash("Inputs initialized")
        self.col_scheme = select_scheme('default')
        return

    def run(self):
        debug("Display thread started")
        while True:
            sleep(0.01)
            m = self.get_cmds()
            if m.get('cmd') != None:
                debug(m)
                self.button_bus.put(m)
            if not self.led_bus.empty():
                status, led_grid = self.led_bus.get()
                self.draw_all(status, led_grid)

        return

    def read_gbl_button(self):
        return not self.gbl_button.value

    def read_ins_button(self):
        return not self.ins_button.value

    def get_cmds(self):
        try:
            self.trellis.sync()  # TODO undo? Fails if called too often
        except Exception as e:
            debug("HW error: {}".format(str(e)))
        m = {'cmd': None}
        if self.read_gbl_button():
            if self.state != 'gbl_cfg':
                m['cmd'] = "CONFIG_A"
                self.state = 'gbl_cfg'
            else:
                self.state = 'play'
        elif self.read_ins_button():
            if self.state != 'ins_cfg':
                m['cmd'] = "CONFIG_B"
                self.state = 'ins_cfg'
            else:
                self.state = 'play'
        return m

    def draw_all(self, status, led_grid):
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
                    diffs.append((x, y, self.led_matrix[x][y]))
                self.old_led_matrix[x][y] = self.led_matrix[x][y]
        for diff in diffs:
            self.trellis.color(diff[0], diff[1], diff[2])
            sleep(0.001)
        if len(diffs) > 0:
            if not AUTO_WRITE:
                for ts in self.trellis._trelli:
                    for t in ts:
                        t.pixels.show()
        return

    def draw_note_grid(self, led_grid):
        for x in range(len(led_grid)):
            for y in range(len(led_grid[x])):
                color = self.col_scheme.get_color(led_grid[x][y], x, y)
                # col = c.PALLETE[led_grid[x][y]]
                self.led_matrix[x][self.grid_h-1-y] = color
        return

    def make_cb(self):
        def button_cb(xcoord, ycoord, edge):
            if edge == NeoTrellis.EDGE_RISING:
                self.button_bus.put({'cmd': 'note', 'x': xcoord, 'y': self.grid_h-1-ycoord})
            return
        return button_cb

    def draw_load_screen(self):
        return
