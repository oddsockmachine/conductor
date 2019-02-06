from constants import *

class ChordSequencer(object):
    """docstring for ChordSequencer."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(ChordSequencer, self).__init__()
        if not isinstance(ins_num, int):
            print("ChordSequencer num {} must be an int".format(ins_num))
            exit()
