#coding=utf-8
from instruments.instrument import Instrument
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALE_INTERVALS, KEYS
import mido
from random import choice, random, randint

class Transformer(object):
    """docstring for Transformer."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1, bars=W/4, height=H):
        super(Transformer, self).__init__()
        if not isinstance(ins_num, int):
            print("Transformer num {} must be an int".format(ins_num))
            exit()
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        # logging.info(mport)
        self.height = height
        self.bars = bars #min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.prev_loc_beat = 0
        self.local_beat_position = 0  # Beat position due to instrument speed, which may be different to other instruments
        self.speed = speed  # Relative speed of this instrument compared to global clock
        self.isdrum = False  # Chromatic instrument for drum tracks
        self.random_pages = False  #  Pick page at random
        self.sustain = True  # Don't retrigger notes if this is True
        self.chaos = 0.0  # Add some randomness to notes
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
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, height)  # Function is cached for convenience

    def update_chaos(self, dir):
        if dir == 1:
            self.chaos += 0.01
        elif self.chaos > 0.01:
            self.chaos -= 0.01
        return

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
        self.octave = up_down  #TODO handle up and down as well as octave number
        # self.octave = (self.octave + up_down) % 7
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def get_curr_page(self):
        return self.pages[self.curr_page_num]

    def get_page_stats(self):
        return [x.repeats for x in self.pages]

    def add_page(self, pos=True):
        '''Add or insert a new blank page into the list of pages'''
        if len(self.pages) == 8:
            return False
        if pos:
            self.pages.insert(self.curr_page_num+1, Note_Grid(self.bars, self.height))
        else:
            self.pages.append(Note_Grid(self.bars, self.height))
        return True

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

    def get_notes_from_curr_beat(self):
        self.get_curr_page().get_notes_from_beat(self.local_beat_position)
        return

    def get_curr_page_leds(self):
        return

    def get_curr_page_grid(self):
        return self.get_curr_page().note_grid

    def inc_page_repeats(self, page):
        '''Increase how many times the current page will loop'''
        if page > len(self.pages)-1:
            return False
        self.pages[page].inc_repeats()
        return True

    def dec_page_repeats(self, page):
        '''Reduce how many times the current page will loop'''
        if page > len(self.pages)-1:
            return False
        self.pages[page].dec_repeats()
        return True

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            # Intermediate beat for this instrument, do nothing
            return
        self.local_beat_position = local
        if self.is_page_end():
            self.advance_page()
        new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def calc_local_beat(self, global_beat):
        '''Calc local_beat_pos for this instrument'''
        div = self.get_beat_division()
        local_beat = int(global_beat / div) % self.width
        # logging.info("g{} d{} w{} l{}".format(global_beat, div, self.width, local_beat))
        return local_beat

    def is_page_end(self):
        return self.local_beat_position == 0

    def has_beat_changed(self, local_beat):
        if self.prev_loc_beat != local_beat:
            self.prev_loc_beat = local_beat
            return True
        self.prev_loc_beat = local_beat
        return False

    def get_next_page_num(self):
        '''Return the number of the next page that has a positive number of repeats
        or return a random page if wanted'''
        if self.random_pages:
            # Create a distribution of the pages and their repeats, pick one at random
            dist = []
            for index, page in enumerate(self.pages):
                for r in range(page.repeats):
                    dist.append(index)
            next_page_num = choice(dist)
            return next_page_num
        for i in range(1, len(self.pages)):
            # Look through all the upcoming pages
            next_page_num = (self.curr_page_num + i) % len(self.pages)
            rpts = self.pages[next_page_num].repeats
            # logging.info("i{} p{} r{}".format(i, next_page_num, rpts))
            if rpts > 0:  # This one's good, return it
                return next_page_num
        # All pages including curr_page are zero repeats, just stick with this one
        return self.curr_page_num

    def advance_page(self):
        '''Go to next repeat or page'''
        if self.random_pages:
            # Create a distribution of the pages and their repeats, pick one at random
            dist = []
            for index, page in enumerate(self.pages):
                for r in range(page.repeats):
                    dist.append(index)
            next_page_num = choice(dist)
            self.curr_page_num = next_page_num
            self.curr_rept_num = 0  # Reset, for this page or next page
            return
        self.curr_rept_num += 1  # inc repeat number
        if self.curr_rept_num >= self.get_curr_page().repeats:
        # If we're overfowing repeats, time to go to next available page
            self.curr_rept_num = 0  # Reset, for this page or next page
            self.curr_page_num = self.get_next_page_num()
        return

    def get_beat_division(self):
        return 2**self.speed

    def get_beat_division_str(self):
        return self.speed
        # return {0:'>>>',1:'>>',2:'>',3:'-'}.get(self.speed, 'ERR')

    def change_division(self, div):
        '''Find current instrument, inc or dec its beat division as appropriate'''
        if div == "-":
            if self.speed == 0:
                return
            self.speed -= 1
            return
        if div == "+":
            if self.speed == 4:
                return
            self.speed += 1
            return

        # Direct set
        self.speed = div
        return

    def get_curr_notes(self):
        grid = self.get_curr_page_grid()
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos]]
        if self.chaos > 0:  # If using chaos, switch up some notes
            if beat_notes.count(NOTE_ON) > 0:  # Only if there are any notes in use
                if random() < self.chaos:
                    rand_note = randint(0, self.height-1)
                    beat_notes[rand_note] = NOTE_ON if beat_notes[rand_note] != NOTE_ON else NOTE_OFF
                    # beat_notes = [n if random() < self.chaos else (NOTE_ON if n==NOTE_OFF else NOTE_OFF) for n in beat_notes]
        notes_on = [i for i, x in enumerate(beat_notes) if x == NOTE_ON]  # get list of cells that are on
        return notes_on

    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
        if self.sustain:
            _notes_off = [n for n in notes_off if n not in notes_on]
            _notes_on = [n for n in notes_on if n not in notes_off]
            notes_off = _notes_off
            notes_on = _notes_on
        notes_off = [n for n in notes_off if n<128 and n>0]
        notes_on = [n for n in notes_on if n<128 and n>0]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
            for msg in msgs:
                self.mport.send(msg)

    def save(self):
        saved = {
          "Octave": self.octave,
          "Key": self.key,
          "Scale": self.scale,
          "Pages": [p.save() for p in self.pages],
          "Speed": self.speed,
          "IsDrum": self.isdrum,
          "Sustain": self.sustain,
          "Chaos": self.chaos,
          "RandomRpt": self.random_pages,
        }
        return saved

    def load(self, saved):
        self.octave = saved["Octave"]
        self.key = saved["Key"]
        self.scale = saved["Scale"]
        self.speed = saved["Speed"]
        self.isdrum = saved["IsDrum"]
        self.sustain = saved["Sustain"]
        self.chaos = saved["Chaos"]
        self.random_pages = saved["RandomRpt"]
        self.pages = []
        for p in saved["Pages"]:
            page = Note_Grid(self.bars, self.height)
            print(p)
            page.load(p)
            self.pages.append(page)
        return

    def clear_page(self):
        self.get_curr_page().clear_page()
        return



























import unittest
class TestSequencer(unittest.TestCase):

    def test_instrument(self):
        ins = Sequencer(8, None, "a", "pentatonic", octave=2, bars=4)
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
        ins = Sequencer(8, None, "a", "pentatonic", octave=3, bars=4)
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
        ins = Sequencer(8, None, "a", "pentatonic", octave=3, bars=4)
        ins.touch_note(0,0)
        ins.touch_note(0,1)
        ins.touch_note(0,2)
        ins.touch_note(1,5)
        ins.touch_note(1,6)
        ins.touch_note(1,7)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.local_beat_position, 0)
        ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [5,6,7])
        self.assertEqual(ins.local_beat_position, 1)
        ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [])
        self.assertEqual(ins.local_beat_position, 2)
        self.assertEqual(ins.curr_page_num, 0)  # Still on page 0
        for i in range(14):
            ins.step_beat()
        self.assertEqual(ins.local_beat_position, 0)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, wrapped around
        ins.add_page(1)
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, new page is next
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.local_beat_position, 1)
        self.assertEqual(ins.curr_page_num, 1)  # Should still be on same page, wrapped around
        self.assertEqual(ins.get_curr_notes(), [])
        for i in range(15):
            ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, wrapped around
        self.assertEqual(ins.local_beat_position, 0)

    def test_multi_repeats(self):
        ins = Sequencer(8, None, "a", "pentatonic", octave=3, bars=4)
        ins.touch_note(0,0)
        ins.touch_note(0,1)
        ins.touch_note(0,2)
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        ins.add_page(1)
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 1)
        self.assertEqual(ins.local_beat_position, 1)
        ins.touch_note(1,5)
        ins.touch_note(1,6)
        ins.touch_note(1,7)
        self.assertEqual(ins.get_curr_notes(), [5,6,7])
        for i in range(16):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 0) # Back to page 0
        self.assertEqual(ins.local_beat_position, 1)
        ins.inc_curr_page_repeats()
        self.assertEqual(ins.curr_rept_num, 0)
        for i in range(15):
            ins.step_beat()
        self.assertEqual(ins.get_curr_notes(), [0,1,2])
        self.assertEqual(ins.curr_page_num, 0)  # Should still be on same page, 2nd repeat
        self.assertEqual(ins.local_beat_position, 0)
        self.assertEqual(ins.curr_rept_num, 1)
        for i in range(17):
            ins.step_beat()
        self.assertEqual(ins.curr_page_num, 1)
        self.assertEqual(ins.local_beat_position, 1)
        self.assertEqual(ins.get_curr_notes(), [5,6,7])

    def test_cell_to_midi(self):
        ins1 = Sequencer(8, None, "a", "chromatic", octave=3, bars=4)
        self.assertEqual(ins1.cell_to_midi(0), 57)
        self.assertEqual(ins1.cell_to_midi(1), 58)
        self.assertEqual(ins1.cell_to_midi(2), 59)
        ins2 = Sequencer(8, None, "a", "major", octave=3, bars=4)
        self.assertEqual(ins2.cell_to_midi(0), 57)
        self.assertEqual(ins2.cell_to_midi(1), 59)
        self.assertEqual(ins2.cell_to_midi(2), 61)
        self.assertEqual(ins2.cell_to_midi(3), 62)

    def test_midi_out(self):
        from midi import MockMidiOut
        fake_out = MockMidiOut()
        ins = Sequencer(9, fake_out, "a", "chromatic", octave=3, bars=4)
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
