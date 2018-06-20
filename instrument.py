#coding=utf-8
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALES, KEYS
import mido

class Instrument(object):
    """docstring for Instrument."""
    def __init__(self, ins_num, mport, key, scale, octave=1, bars=W/4, height=H):
        super(Instrument, self).__init__()
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        logging.info(mport)

        self.height = height
        self.bars = bars #min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.beat_position = 0
        self.isdrum = False
        self.sustain = False  # TODO don't retrigger notes if this is True
        self.pages = [Note_Grid(self.bars, self.height)]
        if key not in KEYS:
            print('Requested key {} not known'.format(key))
            exit()
        self.key = key
        if scale not in SCALES.keys():
            print('Requested scale {} not known'.format(scale))
            exit()
        self.scale = scale
        self.octave = octave  # Starting octave
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, height)

    def set_key(self, key):
        self.key = key
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def set_scale(self, scale):
        self.scale = scale
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def change_octave(self, up_down):
        self.octave = (self.octave + up_down) % 7
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def get_curr_page(self):
        return self.pages[self.curr_page_num]

    def get_page_stats(self):
        return [x.repeats for x in self.pages]

    def add_page(self, pos=True):
        '''Add or insert a new blank page into the list of pages'''
        if len(self.pages) == 16:
            return False
        if pos:
            self.pages.insert(self.curr_page_num+1, Note_Grid(self.bars, self.height))
        else:
            self.pages.append(Note_Grid(self.bars, self.height))
        return True

    def set_next_page(self):
        '''Override and skip to a particular page when the beat reaches the end'''
        return

    def cell_to_midi(self, cell):
        '''convert a cell height to a midi note based on key, scale, octave'''
        midi_note_num = self.note_converter[cell]
        return midi_note_num

    def touch_note(self, x, y):
        '''touch the x/y cell on the current page'''
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.touch_note(x, y)
        return True

    def add_note(self, x, y, page=False):
        '''force-on a x/y cell on the current page'''
        # if not page:
        #     page = self.get_curr_page()
        # if page > len(self.pages):
        #     logging.warning('Requested page {} > {}'.format(page, len(self.pages)))
        #     return False
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.add_note(x, y)
        return True

    def del_note(self, x, y):
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.del_note(x, y)
        return True

    def get_notes_from_curr_beat(self):
        self.get_curr_page().get_notes_from_beat(self.beat_position)
        return

    def get_curr_page_leds(self):
        return

    def get_curr_page_grid(self):
        # page = self.get_curr_page()
        return self.get_curr_page().note_grid

    def print_curr_page_notes(self):
        self.get_curr_page().print_notes()
        return
        grid = self.get_curr_page_grid()
        # display = {0: '. ', 1: '░░', 2:'▒▒', 3:'▓▓'}
        for c, column in enumerate(grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                if r == self.beat_position: # and display[y] != LED_ACTIVE:
                    print(DISPLAY[LED_SELECT], end='')
                else:
                    print(DISPLAY[cell], end='')
            print('')
        print('')

    def inc_curr_page_repeats(self):
        '''Increase how many times the current page will loop'''
        self.get_curr_page().inc_repeats()
        return

    def dec_curr_page_repeats(self):
        '''Reduce how many times the current page will loop'''
        self.get_curr_page().dec_repeats()
        return

    def step_beat(self, beat=None):
        '''Increment the beat counter, and do the math on pages and repeats'''
        # if beat:
        #     self.beat_position = beat
        #     return
        self.beat_position += 1
        if self.beat_position == self.width:
            self.beat_position = 0
            # print("page done")
            self.curr_rept_num += 1
            if self.curr_rept_num >= self.get_curr_page().repeats:
                self.curr_rept_num = 0
                self.curr_page_num += 1
                # print("next page")
                self.curr_page_num %= len(self.pages)
        # print("b{}/{}, p{}/{}, r{}/{}".format(self.beat_position, self.width, self.curr_page_num+1, len(self.pages), self.curr_rept_num+1, self.get_curr_page().repeats))
        new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def get_curr_notes(self):
        grid = self.get_curr_page_grid()
        beat_pos = self.beat_position
        # beat_notes = [row[beat_pos] for row in grid][::-1]  # extract column from grid
        beat_notes = grid[beat_pos]
        notes_on = [i for i, x in enumerate(beat_notes) if x == NOTE_ON]  # get list of cells that are on
        return notes_on


    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
            for msg in msgs:
                self.mport.send(msg)





import unittest
class TestInstrument(unittest.TestCase):

    def test_instrument(self):
        ins = Instrument(8, None, "a", "pentatonic", octave=2, bars=4)
        self.assertTrue(ins.touch_note(0,1))
        self.assertTrue(ins.touch_note(0,3))
        self.assertTrue(ins.touch_note(0,5))
        self.assertTrue(ins.touch_note(2,6))
        self.assertTrue(ins.touch_note(2,7))
        self.assertTrue(ins.touch_note(2,8))
        self.assertFalse(ins.touch_note(-1,-1))
        self.assertFalse(ins.touch_note(99,-99))
        self.assertTrue(ins.touch_note(1,0))
        self.assertTrue(ins.touch_note(2,0))
        ins.inc_curr_page_repeats()
        ins.add_page(1)
        ins.step_beat()

    def test_multi_pages(self):
        ins = Instrument(8, None, "a", "pentatonic", octave=3, bars=4)
        self.assertEqual(len(ins.pages), 1)
        self.assertEqual(ins.curr_page_num, 0)
        ins.touch_note(0,0)
        ins.touch_note(0,1)
        ins.touch_note(0,2)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])

        ins.add_page(1)  # Add a page _after_ current page
        self.assertEqual(ins.curr_page_num, 0)
        ins.touch_note(0,4)  # Still on first page
        ins.touch_note(0,5)
        ins.touch_note(0,6)
        self.assertEqual(len(ins.pages), 2)
        self.assertEqual(ins.get_curr_notes(), [0,1,2,4,5,6])

        ins.add_page(0)  # Add a page _before_ current page
        self.assertEqual(ins.curr_page_num, 0)  # on new page, prev page pushed back
        self.assertEqual(len(ins.pages), 3)
        ins.touch_note(0,3)
        ins.touch_note(0,6)
        ins.touch_note(0,9)
        self.assertEqual(ins.get_curr_notes(), [3,6,9])

    def test_stepping_and_pages(self):
        ins = Instrument(8, None, "a", "pentatonic", octave=3, bars=4)
        ins.touch_note(0,0)
        ins.touch_note(0,1)
        ins.touch_note(0,2)
        ins.touch_note(1,5)
        ins.touch_note(1,6)
        ins.touch_note(1,7)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.beat_position, 0)
        ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [5,6,7])
        self.assertEqual(ins.beat_position, 1)
        ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [])
        self.assertEqual(ins.beat_position, 2)
        self.assertEqual(ins.curr_page_num, 0)  # Still on page 0
        for i in range(14):
            ins.step_beat()
        self.assertEqual(ins.beat_position, 0)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, wrapped around
        ins.add_page(1)
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, new page is next
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.beat_position, 1)
        self.assertEqual(ins.curr_page_num, 1)  # Should still be on same page, wrapped around
        self.assertEqual(ins.get_curr_notes(), [])
        for i in range(15):
            ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, wrapped around
        self.assertEqual(ins.beat_position, 0)

    def test_multi_repeats(self):
        ins = Instrument(8, None, "a", "pentatonic", octave=3, bars=4)
        ins.touch_note(0,0)
        ins.touch_note(0,1)
        ins.touch_note(0,2)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        ins.add_page(1)
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 1)
        self.assertEqual(ins.beat_position, 1)
        ins.touch_note(1,5)
        ins.touch_note(1,6)
        ins.touch_note(1,7)
        self.assertEqual(ins.get_curr_notes(), [5,6,7])
        for i in range(16):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 0) # Back to page 0
        self.assertEqual(ins.beat_position, 1)
        ins.inc_curr_page_repeats()
        self.assertEqual(ins.curr_rept_num, 0)
        for i in range(15):
            ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, 2nd repeat
        self.assertEqual(ins.beat_position, 0)
        self.assertEqual(ins.curr_rept_num, 1)
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 1)
        self.assertEqual(ins.beat_position, 1)
        self.assertEqual(ins.get_curr_notes(), [5,6,7])

    def test_cell_to_midi(self):
        ins1 = Instrument(8, None, "a", "chromatic", octave=3, bars=4)
        self.assertEqual(ins1.cell_to_midi(0), 57)
        self.assertEqual(ins1.cell_to_midi(1), 58)
        self.assertEqual(ins1.cell_to_midi(2), 59)
        ins2 = Instrument(8, None, "a", "major", octave=3, bars=4)
        self.assertEqual(ins2.cell_to_midi(0), 57)
        self.assertEqual(ins2.cell_to_midi(1), 59)
        self.assertEqual(ins2.cell_to_midi(2), 61)
        self.assertEqual(ins2.cell_to_midi(3), 62)

    def test_midi_out(self):
        from midi import MockMidiOut
        fake_out = MockMidiOut()
        ins = Instrument(9, fake_out, "a", "chromatic", octave=3, bars=4)
        ins.touch_note(1,0)
        ins.touch_note(1,1)
        ins.touch_note(2,14)
        ins.touch_note(2,15)
        ins.step_beat()
        # print(fake_out.buffer)
        self.assertEqual(len(fake_out.buffer), 2)
        notes = fake_out.get_output()
        self.assertEqual(len(notes), 2)
        note1 = notes[0]
        note2 = notes[1]
        self.assertEqual(len(fake_out.buffer), 0)
        self.assertEqual(note1.type, 'note_on')
        self.assertEqual(note1.channel, 9)
        self.assertEqual(note1.note, 57)
        self.assertEqual(note2.note, 58)
        ins.step_beat()
        notes = fake_out.get_output()
        note3 = notes[0]
        note4 = notes[1]
        note5 = notes[2]
        note6 = notes[3]
        self.assertEqual(note3.type, 'note_off')
        self.assertEqual(note3.note, 57)
        self.assertEqual(note4.type, 'note_off')
        self.assertEqual(note4.note, 58)
        self.assertEqual(note5.type, 'note_on')
        self.assertEqual(note5.note, 71)
        self.assertEqual(note6.type, 'note_on')
        self.assertEqual(note6.note, 72)

if __name__ == '__main__':
    unittest.main()
