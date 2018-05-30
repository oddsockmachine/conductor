from constants import *

class Note_Grid(object):
    """docstring for Note_Grid."""
    def __init__(self, bars=4, height=H):
        super(Note_Grid, self).__init__()
        self.bars = min(bars, 4)  # Option to reduce number of bars < 4
        self.height = H
        self.width = self.bars * 4
        # A W x H grid to store notes on
        self.note_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]
        self.repeats = 1
        # self.key = "A"
        # self.key = "pentatonic"
        # self.octave = 2  # Starting octave

    def touch_note(self, x, y, on_off):
        if x > self.width:
            logging.warning('Requested {} > {}'.format(x, self.width))
            return
        if y > H:
            logging.warning('Requested {} > {}'.format(y, self.height))
            return
        if y < 0:
            logging.warning('Requested {} < 0'.format(y))
            return
        if x < 0:
            logging.warning('Requested {} < 0'.format(y))
            return
        if on_off not in [NOTE_ON, NOTE_OFF]:
            logging.warning('Note state {} not valid'.format(on_off))
            return
        self.note_grid[x][y] = on_off
        pass

    def add_note(self, x, y):
        self.touch_note(x, y, NOTE_ON)
        return

    def del_note(self, x, y):
        self.touch_note(x, y, NOTE_OFF)
        return

    def get_notes_from_beat(self, beat):
        if beat > self.width:
            logging.warning('Beat {} > {}'.format(beat, self.width))
            return
        return self.note_grid[beat]


if __name__ == '__main__':
    notes = Note_Grid()
    notes.touch_note(1,1,NOTE_ON)
    notes.touch_note(2,2,NOTE_OFF)
    notes.add_note(3,3)
    notes.del_note(4,4)
    print(notes.get_notes_from_beat(1))
    print(notes.get_notes_from_beat(2))
    print(notes.get_notes_from_beat(3))
    print(notes.get_notes_from_beat(4))
