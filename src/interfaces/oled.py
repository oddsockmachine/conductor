from threading import Thread
from constants import debug, TICK, BEAT
from time import sleep
from random import randint
from buses import OLED_bus

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
            msg = self.OLED_bus.get()
            screen = msg['screen']  # Which screen to send txt to
            # Send switch msg to i2c mux
            
            sleep(1)
            
        return