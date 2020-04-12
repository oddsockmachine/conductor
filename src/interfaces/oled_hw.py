# Import all board pins.
from board import SCL, SDA
import busio
from time import sleep
# Import the SSD1306 module.
from sh1106 import SH1106_I2C
from x_adafruit_ssd1306 import SSD1306_I2C as SH1106_I2C
# import Mux
import adafruit_tca9548a
from pykka import ThreadingActor
from PIL import Image, ImageDraw, ImageFont
from buses import OLED_bus
from interfaces.oled_abstract import OLED_abstract


class OLED_Screens(ThreadingActor, OLED_abstract):
    """4x OLED screens
    Send text/animations to each"""
    def __init__(self, num_screens):
        super().__init__()
        self.OLED_bus = OLED_bus
        self.i2c = None
        self.num_screens = num_screens
        self.screens = []
        for i in range(num_screens):
            oled = OLED.start(i).proxy()
            self.screens.append(oled)

    def text(self, screen_num, text):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        if screen_num >= self.num_screens:
            return
        self.screens[screen_num].text(text)
        return

    def get_text(self):
        lines = [s.get_text().get() for s in self.screens]
        return lines


class OLED(ThreadingActor):
# class OLED():
    def __init__(self,id, i2c):
        super().__init__()
        self.id = 0
        self.w = 128
        self.h = 64
        self.max_lines = 7
        print(i2c)
        self.i2c = i2c
        self.style = ""
        self.SH1106 = SH1106_I2C(self.w, self.h, self.i2c)#, addr=0x70)
        self.image = Image.new('1', (self.w, self.h))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.w, self.h), outline=0, fill=0)
        self.font = ImageFont.load_default()
        self.SH1106.fill(0)
        self.SH1106.show()
        return

    def _write_lines(self, text_lines):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        text_lines = text_lines[:self.max_lines]
        for i in range(self.max_lines):
            if i >= len(text_lines):
                break
            self.draw.text((2, 1+(i*8)), self._truncate_text(text_lines[i]), font=self.font, fill=255)
        return

    def _background(self):
        self.draw.rectangle((0, 0, self.w - 2, self.h - 1 ), outline=1, fill=0)
        return

    def _truncate_text(self, text):
        return text[:(int(self.w/6))-1]

    def _display(self):
        self.SH1106.image(self.image)
        self.SH1106.show()
        return

    def set_style(self, style):
        # TODO What about scrolling text? Menu items?
        # TODO Different modes? Menu, title, info, graph
        return

    def clear(self):
        self.draw.rectangle((0, 0, self.w, self.h), outline=0, fill=0)
        return
 
    def text(self, text_lines):
        self.clear()
        self._background()
        self._write_lines(text_lines)
        self._display()
        return

    def menu(self, text_lines, highlight_line):
        self.clear()
        self._background()
        self._write_lines(text_lines)
        i = highlight_line
        self.draw.rectangle((0, (i)*8+2, self.w-2, ((i+1)*8+2)), outline=1, fill=1)
        self.draw.text((2, 1+(i*8)), self._truncate_text(text_lines[i]), font=self.font, fill=0)

        self._display()
        return
