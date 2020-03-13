from constants import debug
from board import SCL, SDA
import busio
debug("Creating i2c bus")
I2C_BUS = busio.I2C(SCL, SDA)
debug("Done")
