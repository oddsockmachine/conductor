from constants import *

class Note_Grid(object):
    """A grid of notes, also a page of music."""
    def __init__(self, bars=int(W/4), height=H):
        super(Note_Grid, self).__init__()
        self.bars = min(bars, 8)  # Option to reduce number of bars < 4
        self.height = height
        self.width = self.bars * 4
        # A W x H grid to store notes on
        # grid is a list of columns of notes
        # x gives you the column, y gives the note - 0 being low, 15+ being high
        self.note_grid = [[LED_BLANK for y in range(self.height)] for x in range(self.width)]
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
            logging.warning('Requested {} > {}'.format(x, self.width))
            return False
        if y >= H:
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
        '''touch/invert a note status. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        # y = (self.height - y) - 1
        curr_note = self.note_grid[x][y]
        if curr_note == NOTE_ON:
            self.note_grid[x][y] = NOTE_OFF
        if curr_note == NOTE_OFF:
            self.note_grid[x][y] = NOTE_ON
        return True

    def add_note(self, x, y):
        '''add a note. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        # y = (self.height - y) - 1
        self.note_grid[x][y] = NOTE_ON
        return True

    def del_note(self, x, y):
        '''remove a note. x = beat/time, y = pitch'''
        if not self.validate_touch(x, y):
            return False
        # y = self.height - y - 1
        self.note_grid[x][y] = NOTE_OFF
        return True

    def get_notes_from_beat(self, beat):
        if beat > self.width:
            logging.warning('Beat {} > {}'.format(beat, self.width))
            return
        # y = self.height - y - 1
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

    def print_notes(self):
        for y in range(self.height):
            for x in range(self.width):
                print(DISPLAY[self.get_note_by_pitch(x, self.height - y -1)], end='')
            print('')
        print('')

    def save(self):
        saved_grid = []
        for y in range(self.height):
            acc = 0
            for x in range(self.width):
                n = (self.get_note_by_pitch(x, self.height - y -1) != NOTE_OFF)
                if n:
                    acc += 2**x
            saved_grid.append(acc)
        return {"Grid": saved_grid, "Repeats": self.repeats}

import unittest
class TestNoteGrid(unittest.TestCase):

    def test_notes(self):
        notes = Note_Grid()
        self.assertEqual(len(notes.note_grid), 16)
        self.assertEqual(len(notes.note_grid[0]), 16)
        self.assertTrue(notes.touch_note(0,0))
        self.assertTrue(notes.touch_note(0,15))
        self.assertTrue(notes.touch_note(0,14))
        self.assertTrue(notes.touch_note(0,13))
        self.assertTrue(notes.touch_note(1,13))
        self.assertTrue(notes.touch_note(2,10))
        self.assertTrue(notes.touch_note(2,2))
        self.assertTrue(notes.add_note(3,3))
        self.assertTrue(notes.del_note(4,4))
        self.assertTrue(notes.del_note(2,2))

        self.assertEqual(notes.get_notes_from_beat(0), [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3])
        self.assertEqual(notes.get_notes_from_beat(1), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0])
        self.assertEqual(notes.get_notes_from_beat(2), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0])
        self.assertEqual(notes.get_notes_from_beat(3), [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(notes.get_notes_from_beat(4), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        print(notes.note_grid)
        print(notes.print_notes())
        self.assertFalse(notes.touch_note(99,99))
        self.assertFalse(notes.touch_note(1,99))
        self.assertFalse(notes.touch_note(99,1))
        self.assertFalse(notes.touch_note(-1,1))
        self.assertFalse(notes.touch_note(1,-1))

        self.assertFalse(notes.get_note_by_pitch(0,16))
        self.assertFalse(notes.get_note_by_pitch(16,0))
        self.assertFalse(notes.get_note_by_pitch(-1,0))
        self.assertFalse(notes.get_note_by_pitch(1,-1))
        self.assertEqual(notes.get_note_by_pitch(0,15), NOTE_ON)
        self.assertEqual(notes.get_note_by_pitch(0,14), NOTE_ON)
        self.assertEqual(notes.get_note_by_pitch(0,13), NOTE_ON)
        self.assertEqual(notes.get_note_by_pitch(1,13), NOTE_ON)
        self.assertEqual(notes.get_note_by_pitch(1,11), NOTE_OFF)
        self.assertEqual(notes.get_note_by_position(0,0), NOTE_ON)
        self.assertEqual(notes.get_note_by_position(0,1), NOTE_OFF)
        self.assertEqual(notes.get_note_by_position(2,10), NOTE_ON)
        self.assertEqual(notes.get_note_by_position(1,4), NOTE_OFF)

    def test_save(self):
        notes = Note_Grid()
        self.assertTrue(notes.touch_note(0,15))
        self.assertTrue(notes.touch_note(0,14))
        self.assertTrue(notes.touch_note(0,13))
        self.assertTrue(notes.touch_note(1,13))
        self.assertTrue(notes.touch_note(2,10))
        self.assertTrue(notes.touch_note(7,7))
        self.assertTrue(notes.touch_note(6,6))
        self.assertTrue(notes.touch_note(5,5))
        print(notes.print_notes())
        saved = notes.save()
        print(saved)
        self.assertEqual(saved.get('Grid'), [1, 1, 3, 0, 0, 4, 0, 0, 128, 64, 32, 0, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
