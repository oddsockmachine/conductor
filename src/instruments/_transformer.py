# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class Transformer(Instrument):
    """Transformer
    - Take a sequencer pattern, press one button to mutate by a set amount, another button to save the current state"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Transformer, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Transformer"