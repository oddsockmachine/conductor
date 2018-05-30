from constants import *
from note_grid import Note_Grid

class Instrument(object):
    """docstring for Instrument."""
    def __init__(self, name, key, scale, octave, bars=4, height=H):
        super(Instrument, self).__init__()
        self.name = name
        self.height = height
        self.bars = min(bars, 4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4

        self.curr_page = 0
        self.beat_position = 0
        self.pages = [Note_Grid()]
        self.key = "A"
        self.scale = "pentatonic"
        self.octave = 2  # Starting octave


    def add_page(self, pos=-1):
        self.pages.insert(pos, Note_Grid(self.bars, self.height))
        return


ins = Instrument("foo", "a", "pentatonic", 2)
