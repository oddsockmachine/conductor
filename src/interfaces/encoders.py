from threading import Thread
from constants import debug
from config import encoder_addresses
from time import sleep
from random import randint
from buses import encoder_in_bus, encoder_out_bus
from i2c_bus import I2C_BUS
from i2cEncoderLib import i2cEncoder
from pykka import ThreadingActor

class Dial(Thread):
    """4x encoders.
    Listen for commands to set color or animation (RGB, pulsing, etc)
    Send commands when encoders turn L/R and by how much
    Buttons are connected to GPIO, send pushes on button bus"""
    # TODO Should number of encoders be specified/hardcoded here?
    # TODO Maybe RGB LEDS and Encoder/Button status should be separate threads, to avoid blocking behavior
    def __init__(self):
        Thread.__init__(self, name='Dial')
        self.daemon = True
        self.encoder_in_bus = encoder_in_bus
        self.encoder_out_bus = encoder_out_bus
        # Thread.start()

    def run(self):
        debug("Dial")
        while True:
            # Check interrupt of all 4 encoders
            # If interrupt, read encoder/button state
            sleep(1)
        return
    
    def start(self):
        super(Dial, self).start()
        return self


class RGB(Thread):
    """4x encoders.
    Listen for commands to set color or animation (RGB, pulsing, etc)
    Send commands when encoders turn L/R and by how much
    Buttons are connected to GPIO, send pushes on button bus"""
    # TODO Should number of encoders be specified/hardcoded here?
    # TODO Maybe RGB LEDS and Encoder/Button status should be separate threads, to avoid blocking behavior
    def __init__(self):
        Thread.__init__(self, name='RGB')
        self.daemon = True
        self.encoder_in_bus = encoder_in_bus
        self.state = "pulse"
        self.color = [0,0,0]
        self.brightness = 0
        # TODO use Color library with HSL


    def run(self):
        debug("RGB")
        while True:
            # Check interrupt of all 4 encoders
            # If interrupt, read encoder/button state
            sleep(1)
        return
    
    def start(self):
        super(RGB, self).start()
        return self


class Encoder(ThreadingActor):
    def __init__(self, num, encoder_in_bus, encoder_out_bus):
        # TODO make pykka actor?
        super().__init__()
        self.dial = Dial()
        self.rgb = RGB()
        self.num = num
        self.addr = encoder_addresses.get(num)
        self.i2c_bus = I2C_BUS
        self.encoder_in_bus = encoder_in_bus
        self.encoder_out_bus = encoder_out_bus
        self.encoder_hw = i2cEncoder(self.i2c_bus, self.addr)
        self.encoder_hw.onIncrement = self.on_inc
        self.encoder_hw.onDecrement = self.on_dec
        self.encoder_hw.onButtonPush = self.on_push
        self.encoder_hw.writeFadeRGB(1)
# encoder.writeGP1conf(i2cEncoderLibV2.GP_AN | i2cEncoderLibV2.GP_PULL_DI | i2cEncoderLibV2.GP_INT_DI)  # Configure the GP1 as analog input with the pull-up and the interrupt disable #
# writeRGBCode

    def on_inc(self):
        self.encoder_out_bus.put({'encoder': self.num, 'action': 'inc'})
        return
    def on_dec(self):
        self.encoder_out_bus.put({'encoder': self.num, 'action': 'dec'})
        return
    def on_push(self):
        self.encoder_out_bus.put({'encoder': self.num, 'action': 'push'})
        return
    def set_color(self, color):
        self.encoder_hw.writeRGBCode(color)
    

class Encoder_Group(object):
    def __init__(self):
        return


if __name__ == "__main__":
    enc1 = Encoder(0, encoder_in_bus, encoder_out_bus).start().proxy()
    while True:
        data = encoder_out_bus.get()
        print(data)
