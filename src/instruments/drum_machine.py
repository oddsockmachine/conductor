from constants import *

class DrumMachine(object):
    """docstring for DrumMachine."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(DrumMachine, self).__init__()
        if not isinstance(ins_num, int):
            print("DrumMachine num {} must be an int".format(ins_num))
            exit()
