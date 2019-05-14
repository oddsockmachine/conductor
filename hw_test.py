from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
import random

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

print('ready')
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
            # sleep(wait)
    for ts in trelli:
        for t in ts:
            t.pixels.show()

# set_all(wait, OFF)
print("low")
set_all(wait, LOW)
print("done")
sleep(0.1)
print("off")
set_all(wait, OFF)
print("done")

while True:
    # r = random.randint(0,100)
    # print(r)
    # g = random.randint(r,100)
    # print(g)
    # b = random.randint(r+g,100)
    # print(b)
    color = (random.randint(0,100), random.randint(0,100), random.randint(0,100))
    print(color)
    x = random.randint(0,15)
    y = random.randint(0,15)
    print(x, y)
    trellis.color(x, y, color)
    for ts in trelli:
        for t in ts:
            t.pixels.show()
    sleep(0.5)
