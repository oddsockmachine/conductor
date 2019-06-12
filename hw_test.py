from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
import random

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trellis = NeoTrellis(i2c_bus)

trelli = [
     [NeoTrellis(i2c_bus, False, addr=0x3D)],
    ]

trellis = MultiTrellis(trelli)

for ts in trelli:
    for t in ts:
        print(t)
        print(type(t))
        t.pixels.auto_write = False

print('ready')
wait = 0.05
OFF = (0, 0, 0)
LOW = (5,5,5)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def set_all(wait=0.1, col=YELLOW):
    for x in range(4):
        for y in range(4):
            try:
                trellis.color(x, y, col)
            except:
                print("fail 1")
            # sleep(wait)
    try:
        for ts in trelli:
            for t in ts:
                t.pixels.show()
    except:
        print("fail 2")
    return

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
    color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    # print(color)
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    # print(x, y)
    try:
        trellis.color(x, y, color)
    except:
        print("fail color")
    try:
        for ts in trelli:
            for t in ts:
                t.pixels.show()
    except:
        print("fail show")
    if random.randint(0,1) > 0:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        try:
            trellis.color(x, y, (0, 0, 0))
        except:
            print("fail blank")
    sleep(0.1)
