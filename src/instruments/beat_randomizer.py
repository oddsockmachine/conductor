from constants import *

class BeatRandomizer(object):
    """docstring for BeatRandomizer."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(BeatRandomizer, self).__init__()
        if not isinstance(ins_num, int):
            print("BeatRandomizer num {} must be an int".format(ins_num))
            exit()
