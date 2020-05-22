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
from pykka import ThreadingActor
from PIL import Image, ImageDraw, ImageFont

import abc

class OLED_abstract(abc.ABC):
    @abc.abstractmethod
    def text(self, screen_num, text):
        pass
    @abc.abstractmethod
    def get_text(self):
        pass
    @abc.abstractmethod
    def set_encoder_assignment(self, assignment, screen_num=None):
        pass
    @abc.abstractmethod
    def menu_scroll(self, screen_num, up_down):
        pass
    @abc.abstractmethod
    def create_menu(self, screen_num, items):
        pass
    @abc.abstractmethod
    def get_menu_item(self, screen_num):
        pass
    @abc.abstractmethod
    def touch(self, screen_num):
        pass

class OLED_Screens(ThreadingActor, OLED_abstract):
    """4x OLED screens
    Send text/animations to each"""
    def __init__(self, num_screens, i2c, device_mapping=[0,1,2]):
        super().__init__()
        self.i2c = i2c
        self.num_screens = num_screens
        self.screens = []
        for i in range(num_screens):
            oled = OLED(i, i2c[device_mapping[i]])
            self.screens.append(oled)
        self.assignments = ["" for l in range(self.num_screens)]

    def text(self, screen_num, text):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        if screen_num >= self.num_screens:
            return
        self.screens[screen_num].text(text)
        return

    def get_text(self):
        lines = [s.get_text().get() for s in self.screens]
        return lines

    def set_encoder_assignment(self, assignment, screen_num=None):
        if screen_num is None:
            for i in range(self.num_screens):
                if len(assignment[i]) > 0:
                    self.assignments[i] = assignment[i]
                    self.screens[i].set_encoder_assignment(assignment[i])
            return                
        if screen_num > self.num_screens:
            return
        self.assignments[screen_num] = assignment
        self.screens[screen_num].set_encoder_assignment(assignment)
        return

    def create_menu(self, screen_num, items):
        self.screens[screen_num].create_menu(items)
        return

    def menu_scroll(self, screen_num, up_down):
        self.screens[screen_num].menu_scroll(up_down)
        return

    def get_menu_item(self, screen_num):
        return self.screens[screen_num].get_menu_item().get()

    def touch(self, screen_num):
        return self.screens[screen_num].touch().get()



class OLED(ThreadingActor):
# class OLED():
    def __init__(self, id, i2c):
        super().__init__()
        self.num = id
        self.w = 128
        self.h = 64
        self.max_lines = 7
        print(i2c)
        self.i2c = i2c
        self.menu_mode = False
        self.menu_window_start = 0
        self.menu_window_height = self.max_lines - 1 
        self.highlight_line = 0
        self.assignment = f"_encoder_{self.num}_"
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

    def create_menu(self, items, callbacks=None):
        self.menu_mode = True
        self.menu_items = items
        self.highlight_line = 0
        self.clear()
        self.menu_window_start = 0
        self.menu_window_height = self.max_lines - 1
        self.gen_menu()
        if callbacks:
            self.callbacks = callbacks
        return

    def menu_scroll(self, up_down):
        if not self.menu_mode:
            return
        if up_down == "up" and self.highlight_line > 0:
            self.highlight_line -= 1
        elif up_down == "down" and self.highlight_line < len(self.menu_items) - 1:
            self.highlight_line += 1
        if self.highlight_line >= self.menu_window_start + self.menu_window_height:
            self.menu_window_start += 1
        elif self.highlight_line < self.menu_window_start:
            self.menu_window_start -= 1
        self.gen_menu()
        return

    def get_menu_item(self):
        num = self.highlight_line # + self.menu_window_start
        return (num, self.menu_items[num])

    def touch(self):
        if self.menu_mode:
            return self.get_menu_item()
        else:
            print(f"touched encoder {self.num}")

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)
print(tca)
# oled1 = OLED(2, tca[1]) # .start(2, tca[1]).proxy()
# print(oled1)
# oled2 = OLED(2, tca[0]) # .start(2, tca[0]).proxy()
# print(oled2)
# oled3 = OLED(2, tca[7]) # .start(2, tca[7]).proxy()
# print(oled3)

sleep(1)


screens = OLED_Screens(3, tca, [1,0,7])


screens.text(0, ["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"])
screens.text(1, "here come that boi o shit waddup".split(' '))
screens.text(2, "I'm a little teapot short and stout".split(' '))
sleep(1)


screens.text(1, ["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"])
screens.text(2, "here come that boi o shit waddup".split(' '))
screens.text(0, "I'm a little teapot short and stout".split(' '))

screens.text(2, ["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"])
screens.text(0, "here come that boi o shit waddup".split(' '))
screens.text(1, "I'm a little teapot short and stout".split(' '))

sleep(0.5)
for i in range(7):
    print(i)
    screens.menu(0, ["hello", "world", "123456789012345678901","lol","I'm","in","QUARANTINE!"], i).get()
    screens.menu(1, "here come that boi o shit waddup".split(' '), i).get()
    screens.menu(2, "I'm a little teapot short and stout".split(' '), i).get()
    print(i)

