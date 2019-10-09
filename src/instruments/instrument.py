# coding=utf-8
import constants as c
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup
import mido
from random import choice, random, randint
from copy import deepcopy
from interfaces.lcd import lcd
from buses import midi_out_bus


class Instrument(object):
    """docstring for Instrument."""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Instrument, self).__init__()
        self.type = "Generic Instrument"
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        self.height = 16
        self.width = 16
        self.prev_loc_beat = 0
        self.local_beat_position = 0
        self.speed = speed  # Relative speed of this instrument compared to global clock
        self.key = key
        self.scale = scale
        self.octave = octave  # Starting octave
        self.is_drum = False
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, self.height)
        self.selected_next_page_num = None
        self.edit_page = None  # Track which page we want to show and edit while playback continues

    def restart(self):
        """Set all aspects of instrument back to starting state"""
        self.local_beat_position = 0
        self.selected_next_page_num = 0
        return

    def cell_to_midi(self, cell):
        '''convert a cell height to a midi note based on key, scale, octave'''
        midi_note_num = self.note_converter[cell]
        return midi_note_num

    def set_key(self, key):
        # c.logging.info(f"set key {key}")
        if self.is_drum:
            c.logging.info(self.is_drum)
            self.is_drum = (True, self.scale, key, self.octave)
            c.logging.info(self.is_drum)
            return
        self.key = key  # Converter is a cached lookup, we need to regenerate it
        self.output(self.old_notes, [])
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        lcd.flash("Key {}".format(key))
        return True

    def set_scale(self, scale):
        # c.logging.info(f"set scale {scale}")
        if self.is_drum:
            c.logging.info(self.is_drum)
            self.is_drum = (True, scale, self.key, self.octave)
            c.logging.info(self.is_drum)
            return
        self.scale = scale  # Converter is a cached lookup, we need to regenerate it
        self.output(self.old_notes, [])
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        lcd.flash("Scale {}".format(scale))
        return True

    def change_octave(self, up_down):
        self.octave = up_down  # TODO handle up and down as well as octave number
        self.output(self.old_notes, [])
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def add_page(self, pos=True):
        '''Add or insert a new blank page into the list of pages'''
        if len(self.pages) == 16:
            lcd.flash("Max pages reached")
            return False
        if pos:
            self.pages.insert(self.curr_page_num+1, Note_Grid(self.bars, self.height))
        else:
            self.pages.append(Note_Grid(self.bars, self.height))
        lcd.flash("Added page")
        return True

    def get_curr_page(self):
        return self.pages[self.curr_page_num]

    def get_page_stats(self):
        return [x.repeats for x in self.pages]

    def get_status(self):
        status = {
            'ins_num': self.ins_num+1,
            'ins_total': 16,
            'page_num': self.curr_page_num+1,
            'page_total': len(self.pages),
            'repeat_num': self.curr_rept_num+1,
            'repeat_total': self.get_curr_page().repeats,
            'page_stats': self.get_page_stats(),
            'key': str(self.key),
            'scale': str(self.scale),
            'octave': str(self.octave),
            'type': self.type,
            'division': self.get_beat_division_str(),
            'random_rpt': self.random_pages,
            'sustain': self.sustain,
        }
        return status

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.touch_note(x, y)
        return True

    def get_notes_from_curr_beat(self):
        self.get_curr_page().get_notes_from_beat(self.local_beat_position)
        return

    def get_next_page_num(self):
        '''Return the number of the next page that has a positive number of repeats
        or return a random page if wanted'''
        if self.selected_next_page_num is not None:
            p = self.selected_next_page_num
            return p
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
            self.selected_next_page_num = None
        return

    def get_curr_notes(self):
        grid = self.get_led_grid()
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos]]
        if self.chaos > 0:  # If using chaos, switch up some notes
            if beat_notes.count(c.NOTE_ON) > 0:  # Only if there are any notes in use
                if random() < self.chaos:
                    rand_note = randint(0, self.height-1)
                    beat_notes[rand_note] = c.NOTE_ON if beat_notes[rand_note] != c.NOTE_ON else c.NOTE_OFF
        # beat_notes = [n if random() < self.chaos else (NOTE_ON if n==NOTE_OFF else NOTE_OFF) for n in beat_notes]
        notes_on = [i for i, x in enumerate(beat_notes) if x == c.NOTE_ON]  # get list of cells that are on
        return notes_on

    def get_beat_division(self):
        return 2**self.speed

    def get_beat_division_str(self):
        return self.speed

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

    def has_beat_changed(self, local_beat):
        if self.prev_loc_beat != local_beat:
            self.prev_loc_beat = local_beat
            return True
        self.prev_loc_beat = local_beat
        return False

    def calc_local_beat(self, global_beat):
        '''Calc local_beat_pos for this instrument'''
        div = self.get_beat_division()
        local_beat = int(global_beat / div) % self.width
        return int(local_beat)

    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
        if self.sustain:
            _notes_off = [n for n in notes_off if n not in notes_on]
            _notes_on = [n for n in notes_on if n not in notes_off]
            notes_off = _notes_off
            notes_on = _notes_on
        notes_off = [n for n in notes_off if n < 128 and n > 0]
        notes_on = [n for n in notes_on if n < 128 and n > 0]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if len(msgs) > 0:
            c.debug(msgs)
            midi_out_bus.put(msgs)
        # if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
        #     for msg in msgs:
        #         self.mport.send(msg)

    def default_save_info(self):
        return {
            "type": self.type,
            "octave": self.octave,
            "key": self.key,
            "scale": self.scale,
            "speed": self.speed,
          }

    def save(self):
        return self.default_save_info()

    def load_default_info(self, saved):
        self.type = saved["type"]
        self.octave = saved["octave"]
        self.key = saved["key"]
        self.scale = saved["scale"]
        self.speed = saved["speed"]
        return

    def load(self, saved):
        self.load_default_info(saved)
        return

    def cb_sustain(self, x, y):
        self.sustain = not self.sustain
        lcd.flash("Sustain {}".format(self.sustain))
        return

    def cb_random_pages(self, x, y):
        self.random_pages = not self.random_pages
        lcd.flash("Random {}".format(self.random_pages))
        return

    def cb_speed(self, x, y):
        self.speed = x
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        lcd.flash("Speed {}".format(self.speed))
        return

    def cb_octave(self, x, y):
        self.octave = x
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        lcd.flash("Octave {}".format(self.octave))
        return

    def cb_clip(self, x, y):
        page_num = (4*y) + x
        if page_num+1 > len(self.pages):
            return
        self.selected_next_page_num = page_num
        lcd.flash("Next page {}".format(page_num))
        return

    def cb_fill(self, x, y):
        self.fill = False if self.fill else True
        lcd.flash("Fill {}".format(self.fill))
        return

    def cb_drum(self, x, y):
        if self.is_drum:
            c.logging.info(self.is_drum)
            self.scale = self.is_drum[1]
            self.key = self.is_drum[2]
            self.octave = self.is_drum[3]
            self.is_drum = False
            # c.logging.info(f"Reverting to {self.scale}, {self.key}, {self.octave}")
            # lcd.flash(f"Reverting to {self.scale}")
        else:
            self.is_drum = (True, self.scale, self.key, self.octave)
            c.logging.info("Drum mode")
            c.logging.info(self.is_drum)
            self.scale = 'chromatic'
            self.key = 'c'
            self.octave = 1
            lcd.flash("Drum mode")
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return

    def cb_edit_page(self, x, y):
        if self.edit_page is not None:
            self.edit_page = None
            lcd.flash("Edit mode disabled")
        else:
            self.edit_page = self.curr_page_num
            # lcd.flash(f"Editing page {self.edit_page}")
        return

    def cb_copy_page(self, x, y):
        page = y
        if y >= len(self.pages):
            c.logging.info(self.curr_page_num)
            c.logging.info(str(len(self.pages)))
            self.add_page(pos=False)
            self.pages[self.curr_page_num+1].note_grid = deepcopy(self.pages[self.curr_page_num].note_grid)
            c.logging.info(self.curr_page_num)
            c.logging.info(str(len(self.pages)))
            return

        page_num = (4*y) + x
        self.selected_next_page_num = page_num
        lcd.flash("Copied page {}".format(page))
        return

    def cb_page(self, x, y):
        page = y
        if y >= len(self.pages):
            self.add_page(pos=False)
            lcd.flash("Added page")
            return
        if x == 0:
            if self.pages[y].repeats == 1:
                self.pages[y].repeats = 0
                lcd.flash("Page {} rpt 0".format(page+1))
            else:
                self.pages[y].repeats = 1
                lcd.flash("Page {} rpt 1".format(page+1))
            return
        else:
            self.pages[y].repeats = x + 1
            lcd.flash("Page {} rpt {}".format(page+1, self.pages[y].repeats))
        return
