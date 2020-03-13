# https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306


# Import all board pins.
from board import SCL, SDA
import busio
from time import sleep
# Import the SSD1306 module.
import adafruit_ssd1306
# import Mux
import adafruit_tca9548a

from PIL import Image, ImageDraw, ImageFont


class OLED(object):
    def __init__(self,id, i2c):
        self.id = 0
        self.w = 128
        self.h = 32
        self.max_lines = 4
        self.text = ["" for i in range(self.max_lines)]
        self.i2c = i2c
        self.style = ""
        self.SSD1306_I2C = adafruit_ssd1306.SSD1306_I2C(self.w, self.h, self.i2c)
        self.image = Image.new('1', (self.w, self.h))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.w, self.h), outline=0, fill=0)
        self.font = ImageFont.load_default()
        self.SSD1306_I2C.fill(0)
        self.SSD1306_I2C.show()
        return
    def write(self, text, line_no, style):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        self.text[line_no] = text
        self.display()
        return

    def write_lines(self, text_lines, style):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        self.text_lines = text_lines
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
        self.SSD1306_I2C.fill(0)
        self.SSD1306_I2C.show()
        return

    def display(self):
        print(self.text)
        self.draw.text((0, 0), self.text[0], font=font, fill=255)
        self.draw.text((0, 8), self.text[1], font=font, fill=255)
        self.draw.text((0, 16), self.text[2], font=font, fill=255)
        self.draw.text((0, 24), self.text[3], font=font, fill=255)
        self.SSD1306_I2C.image(image)
        self.SSD1306_I2C.show()
        return


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)
# Create the SSD1306 OLED class.
display = adafruit_ssd1306.SSD1306_I2C(128, 32, tca[0])
display2 = adafruit_ssd1306.SSD1306_I2C(128, 32, tca[1])
oled3 = OLED(2, tca[2])
print(display)
# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)
display.show()
sleep(1)
# Set a pixel in the origin 0,0 position.
display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
display.pixel(127, 31, 1)
display.show()
sleep(1)
display.fill(0)
display.show()
sleep(1)

image = Image.new('1', (display.width, display.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a white background
draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
# Draw a smaller inner rectangle
BORDER = 5
draw.rectangle((BORDER, BORDER, display.width - BORDER - 1, display.height - BORDER - 1),
               outline=0, fill=0)
# Load default font.
font = ImageFont.load_default()
# Draw Some Text
text = "Hello World!"
(font_width, font_height) = font.getsize(text)
draw.text((display.width//2 - font_width//2, display.height//2 - font_height//2),
          text, font=font, fill=255)
# Display image
display.image(image)
display.show()
sleep(1)
exit()



oled3.write("hello", 0, None)
sleep(1)
oled3.write("world", 1, None)
sleep(1)
oled3.write_lines(["howdy", "wurld", ":)", ":D"], None)
sleep(1)
exit()
