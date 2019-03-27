#coding=utf-8
from instruments.instrument import Instrument
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALE_INTERVALS, KEYS
import mido
from random import choice, random, randint

class DrumMachine(Instrument):
    """docstring for DrumMachine."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(DrumMachine, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Drum Machine"
        # self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        # self.mport = mport
        # self.height = 16
        self.bars = 4 #min(bars, W/4)  # Option to reduce number of bars < 4
        # self.width = 16
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.prev_loc_beat = 0
        self.local_beat_position = 0  # Beat position due to instrument speed, which may be different to other instruments
        # self.speed = speed  # Relative speed of this instrument compared to global clock
        self.random_pages = False  #  Pick page at random
        self.sustain = False  # Don't retrigger notes if this is True
        self.pages = [Note_Grid(self.bars, self.height)]
        self.key = 'c'  # TODO find which starting note corresponds to pad 0
        self.scale = 'chromatic'
        self.octave = 0  # Starting octave
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, self.height)  # Function is cached for convenience

    def set_scale(self, scale):
        return # Not used
    def set_key(self, key):
        return # Not used

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

    def get_led_grid(self, state):
        led_grid = []
        grid = self.get_curr_page().note_grid
        for c, column in enumerate(grid):  # columnn counter
            led_grid.append([self.get_led_status(x, c) for x in column])
        return led_grid

    def get_led_status(self, cell, beat_pos):
        '''Determine which type of LED should be shown for a given cell'''
        led = LED_BLANK  # Start with blank / no led
        if beat_pos == self.local_beat_position:
            led = LED_BEAT  # If we're on the beat, we'll want to show the beat marker
            if cell == NOTE_ON:
                led = LED_SELECT  # Unless we want a selected + beat cell to be special
        elif cell == NOTE_ON:
            led = LED_ACTIVE  # Otherwise if the cell is active (touched)
        return led


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
        grid = self.get_led_grid('play')
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos]]
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
          "pages": [p.save() for p in self.pages],
          "sustain": self.sustain,
          "random_rpt": self.random_pages,
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        self.sustain = saved["sustain"]
        self.random_pages = saved["random_rpt"]
        self.pages = []
        for p in saved["pages"]:
            page = Note_Grid(self.bars, self.height)
            page.load(p)
            self.pages.append(page)
        return

    def clear_page(self):
        self.get_curr_page().clear_page()
        return
