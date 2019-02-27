from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis


#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#create the trellis
trellis = NeoTrellis(i2c_bus)

from time import sleep
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x31)],
    [NeoTrellis(i2c_bus, False, addr=0x32), NeoTrellis(i2c_bus, False, addr=0x33), NeoTrellis(i2c_bus, False, addr=0x34), NeoTrellis(i2c_bus, False, addr=0x35)],
    [NeoTrellis(i2c_bus, False, addr=0x36), NeoTrellis(i2c_bus, False, addr=0x37), NeoTrellis(i2c_bus, False, addr=0x38), NeoTrellis(i2c_bus, False, addr=0x39)],
    [NeoTrellis(i2c_bus, False, addr=0x3A), NeoTrellis(i2c_bus, False, addr=0x3B), NeoTrellis(i2c_bus, False, addr=0x3C), NeoTrellis(i2c_bus, False, addr=0x3D)],
    ]

trellis = MultiTrellis(trelli)

for ts in trelli:
    for t in ts:
        print(t)
        print(type(t))
        t.pixels.auto_write = False


wait = 0.05
#some color definitions
OFF = (0, 0, 0)
LOW = (5,5,5)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
from time import sleep
PURPLE = (180, 0, 255)

def set_all(wait=0.1, col=YELLOW):
    for x in range(16):
        for y in range(16):
            trellis.color(x, y, col)
            sleep(wait)
    for ts in trelli:
        for t in ts:
            t.pixels.show()

# set_all(0.5, OFF)
print("low")
set_all(0.5, LOW)
print("off")
set_all(0.5, OFF)
