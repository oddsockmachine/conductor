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


# class OLED(pykka.ThreadingActor):
class OLED():
    def __init__(self,id, i2c):
        super().__init__()
        self.id = 0
        self.w = 128
        self.h = 64
        self.max_lines = 7
        self.text = ["" for i in range(self.max_lines)]
        self.i2c = i2c
        self.style = ""
        self.SH1106 = SH1106_I2C(self.w, self.h, self.i2c)
        self.image = Image.new('1', (self.w, self.h))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.w, self.h), outline=0, fill=0)
        self.font = ImageFont.load_default()
        self.SH1106.fill(0)
        self.SH1106.show()
        return
    def write(self, text, line_no, style=None):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        if line_no > self.max_lines-1:
            # TODO log error
            return
        self.text[line_no] = text
        self.display()
        return

    def write_lines(self, text_lines, style=None):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        print(f"text lines {len(text_lines)}")
        for i in range(len(self.text)):
            print(i)
            if i >= len(text_lines):
                break
            self.text[i] = text_lines[i]
        self.display()
        return

    def highlight(self, line_no):
        return

    def set_style(self, style):
        # TODO What about scrolling text? Menu items?
        # TODO Different modes? Menu, title, info, graph
        return

    def clear(self):
        self.text = ["" for i in range(self.max_lines)]
        # Clear the display. Always call show after changing pixels to make the display update visible!
        self.SH1106.show()
        return

    def truncate_text(self, text):
        return text[:(int(self.w/6))-1]

    def display(self):
        print(self.text)
        # self.draw.rectangle((0, 0, 126, 62), outline=255, fill=0)
        # BORDER = 0
        self.draw.rectangle((0, 0, self.w - 2, self.h - 1 ), outline=1, fill=0)
        for i in range(self.max_lines):
            self.draw.text((2, 1+(i*8)), self.truncate_text(self.text[i]), font=self.font, fill=255)
        self.SH1106.image(self.image)
        self.SH1106.show()
        return


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
# tca = adafruit_tca9548a.TCA9548A(i2c)
# Create the SSD1306 OLED class.
# TODO Hook up a separate i2c bus to the rpi
# display = SH1106_I2C(128, 64, i2c)
# display2 = adafruit_ssd1306.SSD1306_I2C(128, 16, tca[1])
oled3 = OLED(2, i2c)
print(oled3)
# oled3 = OLED(2, tca[2])




# oled3.write("hello", 0, None)
# sleep(0.2)
# oled3.write("world", 1, None)
# sleep(0.2)
oled3.write_lines(["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"], None)
# sleep(0.2)
# exit()
