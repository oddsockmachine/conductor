# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class BeatMaker(Instrument):
    """BeatMaker
    - Each drum instrument has a horizontal track
    - Each horizontal cell is a different pattern (or no pattern) for each instrument
    - Select a set of patterns for each instrument, change on the fly
    - Show hits and highlight beatpos as normal
    - 4x4 grid for saved pattern combos. Touch current to reset, touch other to load next page and save previous"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(BeatMaker, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "BeatMaker"
        self.is_drum = True