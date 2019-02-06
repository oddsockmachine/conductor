#coding=utf-8
from constants import *

class Instrument(object):
    """docstring for GenericInstrument."""
    def __init__(self, ins_num, mport, speed=1, bars=W/4, height=H):
        super(Instrument, self).__init__()
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        self.channel_num = ins_num
        self.height = height
        self.bars = bars #min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.prev_loc_beat = 0
        self.local_beat_position = 0  # Beat position due to instrument speed, which may be different to other instruments
        self.speed = speed  # Relative speed of this instrument compared to global clock
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
