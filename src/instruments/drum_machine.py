# coding=utf-8
from instruments.instrument import Instrument
import constants as c
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup
from screens import drum_cfg_grid_defn, generate_screen, get_cb_from_touch


class DrumMachine(Instrument):
    """Drum Machine
      - Like sequencer, but specifically for drums/samplers
      - Notes are chromatic, to fit 4x4 sample set
      - TODO! on controls page, make it easier to set up multiple pages, select next pages etc (like a "play-clip" mode)
      - Continue work on "clip control". For seq too. Move other controls across, allow 16 pages, 4x4 grid.
      - Clicking one sets curr_page, all other repeats to 0"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(DrumMachine, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Drum Machine"
        self.is_drum = True
        self.bars = 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.prev_loc_beat = 0
        self.local_beat_position = 0
        self.random_pages = False  # Pick page at random
        self.sustain = False  # Don't retrigger notes if this is True
        self.pages = [Note_Grid(self.bars, self.height)]
        self.key = 'c'  # TODO find which starting note corresponds to pad 0
        self.scale = 'chromatic'
        self.octave = 1  # Starting octave
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)

    def set_scale(self, scale):
        return  # Not used

    def set_key(self, key):
        return  # Not used

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

    def get_led_grid(self, state):
        if state == 'play':
            led_grid = []
            grid = self.get_curr_page().note_grid
            for i, column in enumerate(grid):  # columnn counter
                led_grid.append([self.get_led_status(x, i) for x in column])
        elif state == 'ins_cfg':
            led_grid, cb_grid = generate_screen(drum_cfg_grid_defn, {
                'speed': int(self.speed),
                'octave': int(self.octave),
                'pages': [x.repeats for x in self.pages],
                'curr_p_r': (self.curr_page_num, self.curr_rept_num),
                'curr_page': self.curr_page_num,
                'next_page': self.get_next_page_num()})
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
