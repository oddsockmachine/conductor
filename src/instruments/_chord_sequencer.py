# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class ChordSequencer(Instrument):
    """ChordSequencer
    - Sets ControlChange values
    - Multiple pages of sliders
    - Options for slew rate, transitions etc
    - Choose pages of 16 big sliders, 32 small sliders, etc"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(ChordSequencer, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "ChordSequencer"