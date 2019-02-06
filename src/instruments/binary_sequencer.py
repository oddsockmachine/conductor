from constants import *

class BinarySequencer(object):
    """docstring for BinarySequencer."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(BinarySequencer, self).__init__()
        if not isinstance(ins_num, int):
            print("BinarySequencer num {} must be an int".format(ins_num))
            exit()
