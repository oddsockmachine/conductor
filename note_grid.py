from constants import *

class Note_Grid(object):
    """A grid of notes, also a page of music."""
    def __init__(self, bars=4, height=H):
        super(Note_Grid, self).__init__()
        self.bars = min(bars, 8)  # Option to reduce number of bars < 4
        self.height = height
        self.width = self.bars * 4
        # A W x H grid to store notes on
        self.note_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]
        self.repeats = 1
        # self.key = "A"
        # self.key = "pentatonic"
        # self.octave = 2  # Starting octave

    def inc_repeats(self):
        self.repeats += 1
        return

    def dec_repeats(self):
        self.repeats -= 1
        return

    # def touch_note(self, x, y, on_off):
    def validate_touch(self, x, y):
        if x > self.width:
            logging.warning('Requested {} > {}'.format(x, self.width))
            return False
        if y > H:
            logging.warning('Requested {} > {}'.format(y, self.height))
            return False
        if y < 0:
            logging.warning('Requested {} < 0'.format(y))
            return False
        if x < 0:
            logging.warning('Requested {} < 0'.format(y))
            return False
        return True

    def touch_note(self, x, y):
        if not self.validate_touch(x, y):
            return False
        curr_note = self.note_grid[x][y]
        if curr_note == NOTE_ON:
            self.note_grid[x][y] = NOTE_OFF
        if curr_note == NOTE_OFF:
            self.note_grid[x][y] = NOTE_ON
        return True

    def add_note(self, x, y):
        if not self.validate_touch(x, y):
            return False
        self.note_grid[x][y] = NOTE_ON
        return

    def del_note(self, x, y):
        if not self.validate_touch(x, y):
            return False
        self.note_grid[x][y] = NOTE_OFF
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
