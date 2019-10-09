
# https://github.com/adafruit/Adafruit_Python_SSD1306
# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x64-oleds


class LCD(object):
    """docstring for LCD."""

    def __init__(self):
        super(LCD, self).__init__()
        self.line1 = ""
        self.line2 = ""
        self.flash_line = ""

    def setup_hw(self, i2c_bus):
        # self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
        # self.disp.begin()
        # self.disp.clear()
        # self.disp.display()
        return

    def print1(self, text):
        self.line1 = text
        self.render()
        return

    def print2(self, text):
        self.line2 = text
        self.render()
        return

    def render(self):
        # Check for change
        # self.disp.clear()
        # self.disp.display()
        return

    def flash(self, text):
        # Show text briefly, then return to previous
        self.flash_line = text[:20].ljust(20)
        return


lcd = LCD()
