# coding=utf-8
from instruments.instrument import Instrument
import constants as c
from note_grid import Note_Grid
import mido
from screens import seq_cfg_grid_defn, generate_screen, get_cb_from_touch


class Sequencer(Instrument):
    """Grid Sequencer
      - 16x16 sequencer
      - Add pages to extend sequence length
      - Pages can have repeats
      - Pages can be picked randomly, weighted by repeats
      - sequencer could be 15 notes high, one row dedicated to pages/repeats"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Sequencer, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Sequencer"
        self.bars = 4  # min(bars, W/4)  # Option to reduce number of bars < 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.prev_loc_beat = 0
        self.local_beat_position = 0
        self.random_pages = False  # Pick page at random
        self.sustain = True  # Don't retrigger notes if this is True
        self.pages = [Note_Grid(self.bars, self.height)]

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        if state == 'play':
            page = self.get_curr_page()
            if not page.validate_touch(x, y):
                return False
            page.touch_note(x, y)
            return True
        elif state == 'ins_cfg':
            cb_text, _x, _y = get_cb_from_touch(self.cb_grid, x, y)
            if not cb_text:
                return
            cb_func = self.__getattribute__('cb_' + cb_text)  # Lookup the relevant conductor function
            cb_func(_x, _y)  # call it, passing it x/y args (which may not be needed)
            return True

    def get_notes_from_curr_beat(self):
        self.get_curr_page().get_notes_from_beat(self.local_beat_position)
        return

    def get_led_grid(self, state):
        if state == 'play':
            led_grid = []
            grid = self.get_curr_page().note_grid
            for i, column in enumerate(grid):  # columnn counter
                led_grid.append([self.get_led_status(x, i) for x in column])
        elif state == 'ins_cfg':
            led_grid, cb_grid = generate_screen(seq_cfg_grid_defn, {
                'speed': int(self.speed),
                'octave': int(self.octave),
                'pages': [x.repeats for x in self.pages],
                'curr_p_r':  (self.curr_page_num, self.curr_rept_num),
                'curr_page':  self.curr_page_num,
                'next_page':  self.get_next_page_num()})
            self.cb_grid = cb_grid
            return led_grid
        return led_grid

    def get_led_status(self, cell, beat_pos):
        '''Determine which type of LED should be shown for a given cell'''
        led = c.LED_BLANK  # Start with blank / no led
        if beat_pos == self.local_beat_position:
            led = c.LED_BEAT  # If we're on the beat, we'll want to show the beat marker
            if cell == c.NOTE_ON:
                led = c.LED_SELECT  # Unless we want a selected + beat cell to be special
        elif cell == c.NOTE_ON:
            led = c.LED_ACTIVE  # Otherwise if the cell is active (touched)
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

    def is_page_end(self):
        return self.local_beat_position == 0

    def has_beat_changed(self, local_beat):
        if self.prev_loc_beat != local_beat:
            self.prev_loc_beat = local_beat
            return True
        self.prev_loc_beat = local_beat
        return False

    def get_curr_notes(self):
        grid = self.get_led_grid('play')
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos]]
        notes_on = [i for i, x in enumerate(beat_notes) if x == c.NOTE_ON]  # get list of cells that are on
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
        notes_off = [n for n in notes_off if n < 128 and n > 0]
        notes_on = [n for n in notes_on if n < 128 and n > 0]
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
