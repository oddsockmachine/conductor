TODO
Create nice GUI, overlay, buttons, info etc on screen
sequencer shouldn't print anything, just provide grid data structure
controller converts to symbols, adds cursor, positions grid in center, passes
events (button presses etc_ to sequencer


class Controller(object):
    """docstring for Controller."""
    def __init__(self, arg):
        super(Controller, self).__init__()
        self.arg = arg
