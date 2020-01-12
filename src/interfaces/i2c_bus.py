from constants import debug
from board import SCL, SDA
import busio
debug("Creating i2c bus")
i2c_bus = busio.I2C(SCL, SDA)
debug("Done")
