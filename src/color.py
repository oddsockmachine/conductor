

# TODO calculate and return color tuples based on brightness setting
OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 125, 125)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
INDIGO = (180, 0, 255)
PURPLE = (255, 0, 255)
colors  = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, PURPLE]
PALLETE = {0: (1, 1, 1), 1: (3, 2, 0), 2: (18, 7, 0), 3: (18, 7, 1)}


class Colors(object):
    """docstring for Colors."""

    def __init__(self, arg):
        super(Colors, self).__init__()
        self.arg = arg
        self.brightness = 0.5
        self.theme = "A"

        OFF = (0, 0, 0)
        RED = (255, 0, 0)
        ORANGE = (255, 125, 125)
        YELLOW = (255, 150, 0)
        GREEN = (0, 255, 0)
        CYAN = (0, 255, 255)
        BLUE = (0, 0, 255)
        INDIGO = (180, 0, 255)
        PURPLE = (255, 0, 255)
        colors = {"OFF": OFF,
                  "RED": RED,
                  "ORANGE": ORANGE,
                  "YELLOW": YELLOW,
                  "GREEN": GREEN,
                  "CYAN": CYAN,
                  "BLUE": BLUE,
                  "INDIGO": INDIGO,
                  "PURPLE": PURPLE}

        self.scheme = []
        self.lookup = []

    def get(self):
        return

    def set_brightness(self, brightness):
        if 1 < brightness or brightness < 0:
            return
        self.brightness = float(brightness)
        return
