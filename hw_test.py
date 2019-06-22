from time import sleep
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
import random
from colour import Color


def col_to_rgb(col):
    rgb = col.get_rgb()
    return (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))


def gradient_1d(start, stop, steps):
    gradient = list(map(col_to_rgb, start.range_to(stop, steps)))
    return gradient


# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trelli = [[], [], [], []]
addrs = [[0x31, 0x30, 0x2f, 0x2e],
         [0x35, 0x34, 0x33, 0x32],
         [0x36, 0x37, 0x38, 0x39],
         [0x3a, 0x3c, 0x3b, 0x3d]]
# Create trelli sequentially with a slight pause between each
for x, slice in enumerate(addrs):
    for y, addr in enumerate(slice):
        t = NeoTrellis(i2c_bus, False, addr=addr)
        t.pixels.auto_write = False
        trelli[x].append(t)
        sleep(0.2)


sizeY = len(trelli) * 4
sizeX = len(trelli[0]) * 4


trellis = MultiTrellis(trelli)

for ts in trelli:
    for t in ts:
        print(t)
        print(type(t))
        t.pixels.auto_write = False

print('ready')
wait = 0.05
OFF = (0, 0, 0)
LOW = (5, 5, 5)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

red = Color("black")
blue = Color("black")
gradient = gradient_1d(red, blue, sizeX*2)
print(gradient)

def set_all(wait=0.1, col=YELLOW):
    for x in range(sizeX):
        for y in range(sizeY):
            try:
                trellis.color(x, y, gradient[y+x])
            except Exception as e:
                print(e)
                print("fail 1")
            # sleep(wait)
    try:
        for ts in trelli:
            for t in ts:
                t.pixels.show()
    except Exception as e:
        print(e)
        print("fail 2")
    return


print("low")
set_all(wait, LOW)
print("done")
exit(0)
sleep(2)
print("off")
set_all(wait, OFF)
print("done")


while True:
    color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
    # print(color)
    x = random.randint(0, sizeX-1)
    y = random.randint(0, sizeY-1)
    # print(x, y)
    try:
        trellis.color(x, y, color)
    except Exception as e:
        print(e)
        print("fail color")
    try:
        for ts in trelli:
            for t in ts:
                t.pixels.show()
    except Exception as e:
        print(e)
        print("fail show")
    if random.randint(0, 1) > 0:
        x = random.randint(0, sizeX-1)
        y = random.randint(0, sizeY-1)
        try:
            trellis.color(x, y, (0, 0, 0))
        except Exception as e:
            print(e)
            print("fail blank")
    sleep(0.1)
