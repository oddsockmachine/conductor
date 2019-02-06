from constants import *

class DrumDeviation(object):
    """docstring for DrumDeviation."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(DrumDeviation, self).__init__()
        if not isinstance(ins_num, int):
            print("DrumDeviation num {} must be an int".format(ins_num))
            exit()
