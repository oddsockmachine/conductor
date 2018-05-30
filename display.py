from cursor import Cursor
from sequencer import Sequencer

class Selector(object):
    def __init__(self):
        self.rows_selected = []
        self.columns_selected = []


class Display(object):
    def __init__(self, scr):
        self.scr = scr
        self.height = H
        self.width = W
        # self.display_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]
        # self.current_page = 0
        # self.cursor = cursor
        # self.select = select
        # self.notes = notes
        self.k = 1
        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor = Cursor()
        self.sequencer = Sequencer()
        # while True:
            # Run seq in thread
            # seq.print
            # Add display overlay
            # handle inputs

if __name__ == '__main__':
    display = Display(None)
