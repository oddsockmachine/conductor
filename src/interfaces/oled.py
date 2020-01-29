from threading import Thread
from pykka import ThreadingActor
from constants import debug, TICK, BEAT
from time import sleep
from random import randint
from buses import OLED_bus

class OLED_Screens(ThreadingActor):
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

    def write(self, screen_num, line_no, text):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        if screen_num >= self.num_screens:
            return
        self.screens[screen_num].write(line_no, text, style=None)
        return

    def get_text(self):
        lines = [s.get_text().get() for s in self.screens]
        return lines


class OLED(ThreadingActor):
    def __init__(self, num):
        super().__init__()
        # Thread.__init__(self, name='OLED_'+str(num))
        self.num = num
        self.address = 0x00
        self.max_lines = 4
        self.max_chars = 16
        self.text = ["" for l in range(self.max_lines)]
    
    def write(self, line_no, text, style=None):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        if line_no >= self.max_lines:
            return
        self.text[line_no] = text[:self.max_chars]
        return

    def highlight(self, line_no, style):
        return

    def clear(self):
        self.text = ["" for l in range(self.max_lines)]
        return

    def get_text(self):
        return self.text
