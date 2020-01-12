from threading import Thread
from constants import debug, TICK, BEAT
from time import sleep
from random import randint

class OLED_Screens(Thread):
    """4x OLED screens
    Send text/animations to each"""
    def __init__(self, mportin, OLED_bus):
        Thread.__init__(self, name='OLED_Screens')
        self.daemon = True
        self.OLED_bus = OLED_bus

    def run(self):
        debug("OLED_Screens")
        while True:
            # beat = randint(110,120)
            # debug("midi still running")
            sleep(1)
            # self.midi_in_bus.put("x")
        return