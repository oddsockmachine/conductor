from threading import Thread
from constants import debug
from time import sleep
from random import randint
from buses import encoder_in_bus, encoder_out_bus

class Encoder(object):
    def __init__(self):
        self.state = "pulse"
        self.color = [0,0,0]
        self.brightness = 0
        # TODO use Color library with HSL
        pass
    

class Encoder_Inputs(Thread):
    """4x encoders.
    Listen for commands to set color or animation (RGB, pulsing, etc)
    Send commands when encoders turn L/R and by how much
    Buttons are connected to GPIO, send pushes on button bus"""
    # TODO Should number of encoders be specified/hardcoded here?
    # TODO Maybe RGB LEDS and Encoder/Button status should be separate threads, to avoid blocking behavior
    def __init__(self, encoder_out_bus, button_out_bus, i2c_bus):
        Thread.__init__(self, name='Encoder_Inputs')
        self.daemon = True
        self.encoder_in_bus = encoder_in_bus
        self.encoder_out_bus = encoder_out_bus
        self.button_out_bus = button_out_bus
        Thread.start()

    def run(self):
        debug("Encoder_Inputs")
        while True:
            # Check interrupt of all 4 encoders
            # If interrupt, read encoder/button state
            sleep(1)
        return
    
    def start(self):
        super(Encoder_Inputs, self).start()
        return self


class Encoder_RGB(Thread):
    """4x encoders.
    Listen for commands to set color or animation (RGB, pulsing, etc)
    Send commands when encoders turn L/R and by how much
    Buttons are connected to GPIO, send pushes on button bus"""
    # TODO Should number of encoders be specified/hardcoded here?
    # TODO Maybe RGB LEDS and Encoder/Button status should be separate threads, to avoid blocking behavior
    def __init__(self, encoder_in_bus, i2c_bus):
        Thread.__init__(self, name='Encoder_RGB')
        self.daemon = True
        self.encoder_in_bus = encoder_in_bus

    def run(self):
        debug("Encoder_RGB")
        while True:
            # Check interrupt of all 4 encoders
            # If interrupt, read encoder/button state
            sleep(1)
        return
    
    def start(self):
        super(Encoder_RGB, self).start()
        return self