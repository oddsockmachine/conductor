from threading import Thread
from pykka import ThreadingActor
from constants import debug, TICK, BEAT
from time import sleep
from random import randint
from buses import OLED_bus
from interfaces.oled_abstract import OLED_abstract

# TODO create an ABC/interface for OLED, then implementations for hw and sw

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



class OLED(ThreadingActor):
    def __init__(self, num):
        super().__init__()
        # Thread.__init__(self, name='OLED_'+str(num))
        self.num = num
        self.address = 0x00
        self.max_lines = 7
        self.max_chars = 20
        self.text_lines = ["" for l in range(self.max_lines)]
    
    def text(self, text):
        """Write text to the relevant line in a particular style (highlighted, plain, inverted, etc)"""
        # self.text = ["" for l in range(self.max_lines)]
        text = text[:self.max_lines-1]
        for i in range(self.max_lines-1):
            if i >= len(text):
                break
            self.text_lines[i] = text[i]
        return

    def highlight(self, line_no, style):
        return

    def clear(self):
        self.text_lines = ["" for l in range(self.max_lines)]
        return

    def get_text(self):
        return self.text_lines

    def set_encoder_assignment(self, assignment):
        self.text_lines[-1] = assignment
        return
