from i2cEncoderLib import i2cEncoder
from board import SCL, SDA
import busio
from time import sleep
# i2c_bus = busio.I2C(SCL, SDA)
import smbus2
bus = smbus2.SMBus(1)

def on_inc():
    print("inc")
    return
def on_dec():
    print("dec")
    return
def on_push():
    print("push")
    return





addr1 = 0x0c
enc1 = i2cEncoder(bus, addr1)


enc1.onIncrement = on_inc
enc1.onDecrement = on_dec
enc1.onButtonPush = on_push
enc1.writeFadeRGB(1)
enc1.writeRGBCode(0xaaaa00)
while True:
    print('.')
    sleep(1)