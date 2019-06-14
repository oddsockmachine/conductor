# coding=utf-8
from instruments.drum_deviator import DrumDeviator
import constants as c
from note_grid import Note_Grid
from screens import oct_cfg_grid_defn, generate_screen, get_cb_from_touch


class Octopus(DrumDeviator):
    """Octopus
    - For each separate drum-note/sample/row, the ability to generate a random sequence with specific sparsity/density
    - Each note line can be regenerated at will
    - Create multiple pages once happy with a particular page
    - Bottom 16x8 shows drum sequence. Clicking on a note toggles it manually.
    - TopLeft 8x8 shows sliders for randomness density. Clicking on a value regenerates that track.
    - TopRight 8x8 shows pages and controls. Save, select, clear pages"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Octopus, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Octopus"
        self.bars = 4
        self.pages = [Note_Grid(self.bars, self.height)]
        self.densities = [0 for x in range(8)]

    def apply_control(self, x, y):
        if y >= 8:  # Control touch, but save it in the page, it's easier that way
            y -= 8
            if x < 8:
                self.densities[y] = x
                self.regen(x, y)

    def regen(self, amt, note):
        '''A randomize menu bar has been clicked, regen that bar's notes'''
        gen_notes = [self.calc_chance(amt) for x in range(16)]
        page = self.get_curr_page()
        gen_notes = [{True: c.NOTE_ON, False: c.NOTE_OFF}[note] for note in gen_notes]
        for i, beat in enumerate(page.note_grid):
            beat[note] = gen_notes[i]
        return

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page - either a control, or a note'''
        if state == 'play':
            # Is touch control or note?
            self.apply_control(x, y)
            # Apply touch to current temp page and source page
            self.get_curr_page().touch_note(x, y)
            # self.temp_page.touch_note(x, y)
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
            for i, column in enumerate(grid):
                led_grid.append([self.get_led_status(x, i) for x in column])
            # Draw control sliders
            for y in range(8):
                # reset slider area (removes beat cursor)
                for x in range(16):
                    led_grid[x][y+8] = c.LED_BLANK
                for a in range(self.densities[y]+1):
                    led_grid[a][y+8] = c.LED_ACTIVE
                led_grid[self.densities[y]][y+8] = c.LED_SELECT
                # led_grid[7][y+8] = LED_CURSOR
        elif state == 'ins_cfg':
            led_grid, cb_grid = generate_screen(oct_cfg_grid_defn, {
                'speed': int(self.speed),
                'octave': int(self.octave),
                'pages': [x.repeats for x in self.pages],
                'curr_p_r': (self.curr_page_num, self.curr_rept_num),
                'curr_page': self.curr_page_num,
                'next_page': self.get_next_page_num()
                })
            self.cb_grid = cb_grid
            return led_grid
        return led_grid

    # def advance_page(self):
    #     '''Go to next repeat or page'''
    #     if self.random_pages:
    #         # Create a distribution of the pages and their repeats, pick one at random
    #         dist = []
    #         for index, page in enumerate(self.pages):
    #             for r in range(page.repeats):
    #                 dist.append(index)
    #         next_page_num = choice(dist)
    #         self.curr_page_num = next_page_num
    #         self.curr_rept_num = 0  # Reset, for this page or next page
    #         return
    #     self.curr_rept_num += 1  # inc repeat number
    #     if self.curr_rept_num >= self.get_curr_page().repeats:
    #         # If we're overfowing repeats, time to go to next available page
    #         self.curr_rept_num = 0  # Reset, for this page or next page
    #         self.curr_page_num = self.get_next_page_num()
    #         self.selected_next_page_num = None
    #
    #     # Take control figures from new page, apply to controls
    #     # notes = self.get_curr_page().note_grid
    #     # for y in range(8, 16):
    #         # for x in range(16):
    #             # if notes[x][y] ==c.NOTE_ON:
    #                 # self.apply_control(x, y)
    #     # self.apply_randomness()
    #     return

    # # def get_led_status(self, cell, beat_pos):
    # #     '''Determine which type of LED should be shown for a given cell'''
    # #     led = LED_BLANK  # Start with blank / no led
    # #     if beat_pos == self.local_beat_position:
    # #         led = LED_BEAT  # If we're on the beat, we'll want to show the beat marker
    # #         if cell ==c.NOTE_ON:
    # #             led = LED_SELECT  # Unless we want a selected + beat cell to be special
    # #     elif cell ==c.NOTE_ON:
    # #         led = LED_ACTIVE  # Otherwise if the cell is active (touched)
    # #     return led
    # #
    # # def inc_page_repeats(self, page):
    # #     '''Increase how many times the current page will loop'''
    # #     if page > len(self.pages)-1:
    # #         return False
    # #     self.pages[page].inc_repeats()
    # #     return True
    # #
    # # def dec_page_repeats(self, page):
    # #     '''Reduce how many times the current page will loop'''
    # #     if page > len(self.pages)-1:
    # #         return False
    # #     self.pages[page].dec_repeats()
    # #     return True
    # #
    # # def step_beat(self, global_beat):
    # #     '''Increment the beat counter, and do the math on pages and repeats'''
    # #     local = self.calc_local_beat(global_beat)
    # #     if not self.has_beat_changed(local):
    # #         # Intermediate beat for this instrument, do nothing
    # #         return
    # #     self.local_beat_position = local
    # #     if self.is_page_end():
    # #         self.advance_page()
    # #     new_notes = self.get_curr_notes()
    # #     self.output(self.old_notes, new_notes)
    # #     self.old_notes = new_notes  # Keep track of which notes need stopping next beat
    # #     return
    #
    # def is_page_end(self):
    #     return self.local_beat_position == 0
    #
    # def has_beat_changed(self, local_beat):
    #     if self.prev_loc_beat != local_beat:
    #         self.prev_loc_beat = local_beat
    #         return True
    #     self.prev_loc_beat = local_beat
    #     return False
    #
    # def get_curr_notes(self):
    #     grid = self.temp_page.note_grid
    #     beat_pos = self.local_beat_position
    #     beat_notes = [n for n in grid[beat_pos][:8]]
    #     notes_on = [i for i, x in enumerate(beat_notes) if x == NOTE_ON]  # get list of cells that are on
    #     return notes_on
    #

    # def output(self, old_notes, new_notes):
    #     """Return all note-ons from the current beat, and all note-offs from the last"""
    #     notes_off = [self.cell_to_midi(c) for c in old_notes]
    #     notes_on = [self.cell_to_midi(c) for c in new_notes]
    #     if self.sustain:
    #         _notes_off = [n for n in notes_off if n not in notes_on]
    #         _notes_on = [n for n in notes_on if n not in notes_off]
    #         notes_off = _notes_off
    #         notes_on = _notes_on
    #     notes_off = [n for n in notes_off if n<128 and n>0]
    #     notes_on = [n for n in notes_on if n<128 and n>0]
    #     off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
    #     on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
    #     msgs = off_msgs + on_msgs
    #     if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
    #         for msg in msgs:
    #             self.mport.send(msg)

    def save(self):
        # TODO
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
