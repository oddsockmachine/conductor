from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis


#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#create the trellis
trellis = NeoTrellis(i2c_bus)

trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x31)],
    [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30)]
                    ]
trellis = MultiTrellis(trelli)


#some color definitions
OFF = (0, 0, 0)
LOW = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def set_all(wait=0.1, col=YELLOW):
    for x in range(8):
        for y in range(8):
            trellis.color(x, y, col)
            # sleep(wait)


set_all(0.5, OFF)
set_all(0.5, LOW)
set_all(0.5, OFF)
