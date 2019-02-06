from constants import *

class Droplets(object):
    """docstring for Droplets."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(Droplets, self).__init__()
        if not isinstance(ins_num, int):
            print("Droplets num {} must be an int".format(ins_num))
            exit()
