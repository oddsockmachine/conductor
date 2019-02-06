from constants import *

class Transformer(object):
    """docstring for Transformer."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(Transformer, self).__init__()
        if not isinstance(ins_num, int):
            print("Transformer num {} must be an int".format(ins_num))
            exit()
