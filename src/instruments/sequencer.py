# coding=utf-8
from instruments.instrument import Instrument
import constants as c
from note_grid import Note_Grid
import mido
from screens import seq_cfg_grid_defn, generate_screen, get_cb_from_touch
from buses import midi_out_bus, proxy_registry


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
        OLED_Screens = proxy_registry('OLED_Screens')
        # OLED_Screens.set_encoder_assignment(['Sequencer1', '', 'Sequencer3', 'Sequencer4'])

    # def touch_encoder(self, id, action):
    #     c.debug("Encoder {id} {action}".format(id=id, action=action))
    #     if id == 1 and action == '+':
    #         self.octave += 1
    #     return

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        if state == 'play':
            if self.edit_page is not None:
                page = self.pages[self.edit_page]
            else:
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
            if self.edit_page is not None:
                grid = self.pages[self.edit_page].note_grid
            else:
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
                'edit_page':  self.edit_page,
                'next_page':  self.get_next_page_num()})
            self.cb_grid = cb_grid
            return led_grid
        return led_grid

    def get_led_status(self, cell, beat_pos):
        '''Determine which type of LED should be shown for a given cell'''
        # TODO check for root notes, bar breaks etc here
        led = c.LED_BLANK  # Start with blank / no led
        if beat_pos == self.local_beat_position and self.edit_page is None:
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
