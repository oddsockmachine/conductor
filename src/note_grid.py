import constants as c


class Note_Grid(object):
    """A grid of notes, also a page of music."""

    def __init__(self, bars=int(c.W/4), height=c.H):
        super(Note_Grid, self).__init__()
        self.bars = min(bars, 8)  # Option to reduce number of bars < 4
        self.height = 16
        self.width = 16
        # A W x H grid to store notes on
        # grid is a list of columns of notes
        # x gives you the column, y gives the note - 0 being low, 15+ being high
        self.note_grid = [[c.LED_BLANK for y in range(self.height)] for x in range(self.width)]
        self.repeats = 1

    def inc_repeats(self):
        if self.repeats == 8:
            return False
        self.repeats += 1
        return True

    def dec_repeats(self):
        if self.repeats == 0:
            return False
        self.repeats -= 1
        return True

    def validate_touch(self, x, y):
        if x >= self.width:
            c.logging.warning('Requested {} > {}'.format(x, self.width))
            return False
        if y >= self.height:
            c.logging.warning('Requested {} > {}'.format(y, self.height))
            return False
        if y < 0:
            c.logging.warning('Requested {} < 0'.format(y))
            return False
        if x < 0:
            c.logging.warning('Requested {} < 0'.format(y))
            return False
        return True

    def touch_note(self, x, y):
        '''touch/invert a note status. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        curr_note = self.note_grid[x][y]
        if curr_note == c.NOTE_ON:
            self.note_grid[x][y] = c.NOTE_OFF
        if curr_note == c.NOTE_OFF:
            self.note_grid[x][y] = c.NOTE_ON
        return True

    def add_note(self, x, y):
        '''add a note. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        self.note_grid[x][y] = c.NOTE_ON
        return True

    def del_note(self, x, y):
        '''remove a note. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        self.note_grid[x][y] = c.NOTE_OFF
        return True

    def get_notes_from_beat(self, beat):
        if beat > self.width:
            c.logging.warning('Beat {} > {}'.format(beat, self.width))
            return
        return self.note_grid[beat]

    def get_note_by_pitch(self, x, y):
        '''get a note status. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        # y = self.height - y
        return self.note_grid[x][y]

    def get_note_by_position(self, x, y):
        '''get a note status. x = beat/time, y = row from top'''
        return self.note_grid[x][y]

    # def print_notes(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             print(DISPLAY[self.get_note_by_pitch(x, self.height - y -1)], end='')
    #         print('')
    #     print('')

    def save(self):
        saved_grid = []
        for y in range(self.height):
            acc = 0
            for x in range(self.width):
                n = (self.get_note_by_pitch(x, self.height - y - 1) != c.NOTE_OFF)
                if n:
                    acc += 2**x
            saved_grid.append(acc)
        return {"grid": saved_grid, "repeats": self.repeats}

    def load(self, saved):  # TODO fix this
        self.repeats = saved["repeats"]
        for x, g in enumerate(saved["grid"]):
            # print('{0:0b}'.format(g).zfill(self.height))
            for y, i in enumerate([int(x) for x in list('{0:0b}'.format(g).zfill(self.height))]):
                if i:
                    self.add_note(self.width-y-1, self.height-x-1)
        return

    def clear_page(self):
        self.note_grid = [[c.LED_BLANK for y in range(self.height)] for x in range(self.width)]
        return


# import unittest
# class TestNoteGrid(unittest.TestCase):

    # def test_notes(self):
    #     notes = Note_Grid()
    #     self.assertEqual(len(notes.note_grid), 16)
    #     self.assertEqual(len(notes.note_grid[0]), 16)
    #     self.assertTrue(notes.touch_note(0,0))
    #     self.assertTrue(notes.touch_note(0,15))
    #     self.assertTrue(notes.touch_note(0,14))
    #     self.assertTrue(notes.touch_note(0,13))
    #     self.assertTrue(notes.touch_note(1,13))
    #     self.assertTrue(notes.touch_note(2,10))
    #     self.assertTrue(notes.touch_note(2,2))
    #     self.assertTrue(notes.add_note(3,3))
    #     self.assertTrue(notes.del_note(4,4))
    #     self.assertTrue(notes.del_note(2,2))
    #
    #     self.assertEqual(notes.get_notes_from_beat(0), [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3])
    #     self.assertEqual(notes.get_notes_from_beat(1), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0])
    #     self.assertEqual(notes.get_notes_from_beat(2), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0])
    #     self.assertEqual(notes.get_notes_from_beat(3), [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #     self.assertEqual(notes.get_notes_from_beat(4), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #     print(notes.note_grid)
    #     print(notes.print_notes())
    #     self.assertFalse(notes.touch_note(99,99))
    #     self.assertFalse(notes.touch_note(1,99))
    #     self.assertFalse(notes.touch_note(99,1))
    #     self.assertFalse(notes.touch_note(-1,1))
    #     self.assertFalse(notes.touch_note(1,-1))
    #
    #     self.assertFalse(notes.get_note_by_pitch(0,16))
    #     self.assertFalse(notes.get_note_by_pitch(16,0))
    #     self.assertFalse(notes.get_note_by_pitch(-1,0))
    #     self.assertFalse(notes.get_note_by_pitch(1,-1))
    #     self.assertEqual(notes.get_note_by_pitch(0,15), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_pitch(0,14), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_pitch(0,13), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_pitch(1,13), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_pitch(1,11), NOTE_OFF)
    #     self.assertEqual(notes.get_note_by_position(0,0), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_position(0,1), NOTE_OFF)
    #     self.assertEqual(notes.get_note_by_position(2,10), c.NOTE_ON)
    #     self.assertEqual(notes.get_note_by_position(1,4), NOTE_OFF)

#     def test_save(self):
#         notes = Note_Grid()
#         self.assertTrue(notes.touch_note(0,15))
#         self.assertTrue(notes.touch_note(0,14))
#         self.assertTrue(notes.touch_note(0,13))
#         self.assertTrue(notes.touch_note(1,13))
#         self.assertTrue(notes.touch_note(2,10))
#         self.assertTrue(notes.touch_note(7,7))
#         self.assertTrue(notes.touch_note(6,6))
#         self.assertTrue(notes.touch_note(5,5))
#         print(notes.print_notes())
#         saved = notes.save()
#         print("saved")
#         print(saved)
#         self.assertEqual(saved.get('Grid'), [1, 1, 3, 0, 0, 4, 0, 0, 128, 64, 32, 0, 0, 0, 0, 0])
#
#         notes2 = Note_Grid()
#         notes2.load(saved)
#         print(notes2.print_notes())
#         self.assertTrue(notes2.get_note_by_position(0,15), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(0,14), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(0,13), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(1,13), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(2,10), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(7,7), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(6,6), c.NOTE_ON)
#         self.assertTrue(notes2.get_note_by_position(5,5), c.NOTE_ON)
#         print("!!!!!!!!!!!!!!!")
#
# if __name__ == '__main__':
#     unittest.main()
