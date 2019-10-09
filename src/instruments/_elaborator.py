# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class Elaborator(Instrument):
    """Elaborator
    - Draw a beat/pattern on a page
    - Select which of the page repeats will be elaborated (eg every 4th)
    - Add randomness to that repeat, but only use notes that are already on the page"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Elaborator, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Elaborator"
     