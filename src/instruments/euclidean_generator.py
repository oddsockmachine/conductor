#coding=utf-8
from instruments.drum_deviator import DrumDeviator
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALE_INTERVALS, KEYS
import mido
from random import choice, random, randint
from screens import empty_grid, seq_cfg_grid_defn, generate_screen, get_cb_from_touch

class EuclideanGenerator(DrumDeviator):
    """Euclidean Beat Generator
    - For each drum-note/sample, set a bar length (<16), euclidean density, and offset
    - Bottom 16x8 shows 8 bar lengths, with hits highlighted. Beatpos moves across, or bar rotates? Clicking on a bar determines its bar length
    - TopLeft 8x8 shows sliders for euclidean density. Clicking on a slider sets density
    - TopRight 8x8 shows sliders for offset. Is this necessary?"""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(EuclideanGenerator, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "EuclideanGenerator"
        self.densities = [3 for x in range(8)]
        self.offsets = [2 for x in range(8)]
        self.lengths = [16 for x in range(8)]
        self.curr_notes_pos = [0 for x in range(8)]

    def regen(self, note):
        '''A parameter for this note has changed, regenerate sequence'''
        new_notes = []
        pattern = [NOTE_ON] + [NOTE_OFF for x in range(7-self.densities[note])]
        logging.info(str(pattern))
        repeats = (2+int(16 / self.lengths[note]))
        logging.info(str(repeats))
        _pattern = [NOTE_OFF for x in range(self.offsets[note])]
        for r in range(repeats):
            _pattern.extend(pattern)
        new_notes = _pattern[:16]
        logging.info(str(new_notes))
        page = self.get_curr_page()
        for i, beat in enumerate(page.note_grid[:self.lengths[note]]):
            beat[note] = new_notes[i]
        return

    def apply_control(self, x, y):
        if y >= 8:  # Control touch, but save it in the page, it's easier that way
            y-=8
            if x < 8: # Fire chances
                self.densities[y] = 7 - x
            else:  # Transpose chances
                self.offsets[y] = x - 8
        else:
            self.lengths[y] = x
        self.regen(y)
        return



    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page - either a control, or a note'''
        if state == 'play':
            # Is touch control or note?
            self.apply_control(x, y)
            # Apply touch to current temp page and source page
            self.get_curr_page().touch_note(x, y)
        elif state == 'ins_cfg':
            cb_text, _x, _y = get_cb_from_touch(self.cb_grid, x, y)
            if not cb_text:
                return
            cb_func = self.__getattribute__('cb_' + cb_text)  # Lookup the relevant conductor function
            cb_func(_x, _y)  # call it, passing it x/y args (which may not be needed)
        return True

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            # Intermediate beat for this instrument, do nothing
            return
        self.local_beat_position = local
        note_grid = self.get_curr_page().note_grid
        new_notes = []
        for i, n in enumerate(self.curr_notes_pos):
            n += 1
            if n >= self.lengths[i]:
                n = 0
            self.curr_notes_pos[i] = n
            if note_grid[i][n] == NOTE_ON:
                new_notes.append(n)


        # new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

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
