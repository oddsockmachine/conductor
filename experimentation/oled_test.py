# pip3 install adafruit-circuitpython-ssd1306


# Import all board pins.
from board import SCL, SDA
import busio
from time import sleep
# Import the SSD1306 module.
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont


class OLED(object):
    def __init__(self):
        self.address = 0x00
        self.text = {}
        self.i2c = None
        return
    def write(self, text, line_no, style):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        return
    def highlight(self, line_no, style):
        return
    def clear(self):
        return
    # TODO What about scrolling text? Menu items?
    # TODO Different modes? Menu, title, info, graph
    pass


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d)
# Alternatively you can change the I2C address of the device with an addr parameter:
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)
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



# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
# font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

# # Draw the text
# draw.text((0, 0), 'Hello!', font=font, fill=255)
# draw.text((0, 30), 'Hello!', font=font2, fill=255)
# draw.text((34, 46), 'Hello!', font=font2, fill=255)

# # Display image
# oled.image(image)
# oled.show()