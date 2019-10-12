# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class ChordSequencer(Instrument):
    """ChordSequencer"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(ChordSequencer, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "ChordSequencer"