import smbus2
import RPi.GPIO as GPIO
from time import sleep
import i2cEncoderLib


def EncoderChange():
    encoder.writeLEDG(100)
    print ('Changed: %d' % (encoder.readCounter32()))
    encoder.writeLEDG(0)

def EncoderPush():
    encoder.writeLEDB(100)
    print ('Encoder Pushed!')
    encoder.writeLEDB(0)

def EncoderDoublePush():
    encoder.writeLEDB(100)
    encoder.writeLEDG(100)
    print ('Encoder Double Push!')
    encoder.writeLEDB(0)
    encoder.writeLEDG(0)

def EncoderMax():
    encoder.writeLEDR(100)
    print ('Encoder max!')
    encoder.writeLEDR(0)

def EncoderMin():
    encoder.writeLEDR(100)
    print ('Encoder min!')
    encoder.writeLEDR(0)

def Encoder_INT(self):
    encoder.updateStatus()


GPIO.setmode(GPIO.BCM)
bus = smbus2.SMBus(1)
INT_pin = 4
GPIO.setup(INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

encoder = i2cEncoderLib.i2cEncoder(bus, 0x0C)

encconfig = (i2cEncoderLib.INT_DATA | i2cEncoderLib.WRAP_ENABLE | i2cEncoderLib.DIRE_RIGHT | i2cEncoderLib.IPUP_ENABLE | i2cEncoderLib.RMOD_X1 | i2cEncoderLib.RGB_ENCODER)
encoder.begin(encconfig)

encoder.writeCounter(0)
encoder.writeMax(35)
encoder.writeMin(-20)
encoder.writeStep(1)
encoder.writeAntibouncingPeriod(8)
encoder.writeDoublePushPeriod(5)
encoder.writeGammaRLED(i2cEncoderLib.GAMMA_2)
encoder.writeGammaGLED(i2cEncoderLib.GAMMA_2)
encoder.writeGammaBLED(i2cEncoderLib.GAMMA_2)

encoder.onChange = EncoderChange
encoder.onButtonPush = EncoderPush
encoder.onButtonDoublePush = EncoderDoublePush
encoder.onMax = EncoderMax
encoder.onMin = EncoderMin

encoder.autoconfigInterrupt()
print ('Board ID code: 0x%X' % (encoder.readIDCode()))
print ('Board Version: 0x%X' % (encoder.readVersion()))

encoder.writeRGBCode(0xFF0000)
sleep(0.3)
encoder.writeRGBCode(0x00FF00)
sleep(0.3)
encoder.writeRGBCode(0x0000FF)
sleep(0.3)
encoder.writeRGBCode(0x00)

GPIO.add_event_detect(INT_pin, GPIO.FALLING, callback=Encoder_INT, bouncetime=10)

while True:
    if GPIO.input(INT_pin) == False: #
        Encoder_INT(encoder) #
    pass