# https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306


# Import all board pins.
from board import SCL, SDA
import busio
from time import sleep
# Import the SSD1306 module.
from sh1106 import SH1106_I2C
from x_adafruit_ssd1306 import SSD1306_I2C as SH1106_I2C
# import Mux
import adafruit_tca9548a
# import pykka
from PIL import Image, ImageDraw, ImageFont


class OLED(pykka.ThreadingActor):
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

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)
print(tca)
# Create the SSD1306 OLED class.
# TODO Hook up a separate i2c bus to the rpi
# display = SH1106_I2C(128, 64, i2c)
# display2 = adafruit_ssd1306.SSD1306_I2C(128, 16, tca[1])
oled1 = OLED(2, tca[1])
print(oled1)
oled2 = OLED(2, tca[0])
print(oled2)
oled3 = OLED(2, tca[7])
print(oled3)

sleep(1)



oled1.text(["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"])
oled2.text("here come that boi o shit waddup".split(' '))
oled3.text("I'm a little teapot short and stout".split(' '))
sleep(1)

oled1.text(["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"])
oled2.text("here come that boi o shit waddup".split(' '))
oled3.text("I'm a little teapot short and stout".split(' '))

sleep(0.5)
for i in range(7):
    oled1.menu(["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"], i)
    oled2.menu("here come that boi o shit waddup".split(' '), i)
    oled3.menu("I'm a little teapot short and stout".split(' '), i)
