import time
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis


#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#create the trellis
trellis = NeoTrellis(i2c_bus)

#some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

#this will be called when button events are received
def blink(event):
    #turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = CYAN
    #turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF

for i in range(16):
    #activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    #activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    #set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    #cycle the LEDs on startup
    trellis.pixels[i] = PURPLE
    time.sleep(.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(.05)

while True:
    #call the sync function call any triggered callbacks
    trellis.sync()
    #the trellis can only be read every 17 millisecons or so
    time.sleep(.02)



################################################################################
################################################################################
################################################################################
################################################################################

# trelli = [
#     [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F)],
#     [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x31)]
#     ]
# trellis = MultiTrellis(trelli)

# #some color definitions
# OFF = (0, 0, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 150, 0)
# GREEN = (0, 255, 0)
# CYAN = (0, 255, 255)
# BLUE = (0, 0, 255)
# PURPLE = (180, 0, 255)
#
# #this will be called when button events are received
# def blink(xcoord, ycoord, edge):
#     #turn the LED on when a rising edge is detected
#     if edge == NeoTrellis.EDGE_RISING:
#         trellis.color(xcoord, ycoord, BLUE)
#     #turn the LED off when a rising edge is detected
#     elif edge == NeoTrellis.EDGE_FALLING:
#         trellis.color(xcoord, ycoord, OFF)
#
# for y in range(8):
#     for x in range(8):
#         #activate rising edge events on all keys
#         trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
#         #activate falling edge events on all keys
#         trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
#         trellis.set_callback(x, y, blink)
#         trellis.color(x, y, PURPLE)
#         time.sleep(.05)
#
# for y in range(8):
#     for x in range(8):
#         trellis.color(x, y, OFF)
#         time.sleep(.05)
#
# while True:
#     #the trellis can only be read every 17 millisecons or so
#     trellis.sync()
#     time.sleep(.02)