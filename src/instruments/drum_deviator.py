#coding=utf-8
from instruments.instrument import Instrument
from instruments.drum_machine import DrumMachine
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALE_INTERVALS, KEYS
import mido
from random import choice, random, randint
from copy import deepcopy
from screens import empty_grid, dev_cfg_grid_defn, generate_screen, get_cb_from_touch

class DrumDeviator(DrumMachine):
    """Drum Deviator - Random Deviation Beat Sequencer
    - Draw a beat on a sequencer grid
    - Each drum-note/sample has a separate random chance of suppressing/firing or transposing
    - Show drum sequencer along bottom 16x8, with notes that are modified for this bar highlighted
    - (suppressed: slightly darker - triggered: slightly brighter - transposed: different color)
    - Use the top 16x8 for controls like randomness per note
    - Allow multiple pages per instrument
    - Transposition could/should be predictable, eg to +8 notes
    - Random notes for each bar determined at start of bar
    - Randomness/chaos amount should be per bar, not per note. eg: at low levels, only change a few notes occasionally
    - TODO randomness controls cover all pages - maybe they should be per-page?
    - TODO apply_randomness doesn't show effects on LED grid
    - TODO maybe fire chance shouldn't add notes randomly, only add where there are already other notes"""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(DrumDeviator, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Drum Deviator"
        self.height = 8
        self.fire_chances = [0 for x in range(8)]
        self.transpose_chances = [0 for x in range(8)]
        self.temp_page = Note_Grid(self.bars, self.height)  # Temporary page used for upcoming notes
        self.pages = [Note_Grid(self.bars, self.height)]


        # each time page changes/restarts, calculate random chance of _either_:
        #     suppressing active note
        #     firing quiet note
        #     transposing active note
        # calculated on a per note basis
        # Keep original beat pattern intact for next page
        # show changed notes in different colors
        # two highlighted sets of 8 sliders for fire/suppress and transpose (centre-out? zero lit)
        # Use regular note_grid to save originals, only 8 high
        # Each new page, generate a temp page of notes (16 high) based on calculations
        # But display 8x16 notes and mods

    def apply_control(self, x, y):
        if y >= 8:  # Control touch, but save it in the page, it's easier that way
            y-=8
            if x < 8: # Fire chances
                self.fire_chances[y] = 7 - x
            else:  # Transpose chances
                self.transpose_chances[y] = x - 8

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page - either a control, or a note'''
        if state == 'play':
            # Is touch control or note?
            self.apply_control(x, y)
            # if y >= 8:  # Control touch, but save it in the page, it's easier that way
            #     y-=8
            #     if x < 8: # Fire chances
            #         self.fire_chances[y] = 7 - x
            #     else:  # Transpose chances
            #         self.transpose_chances[y] = x - 8
            #     return True
            # else:
            # Apply touch to current temp page and source page
            self.get_curr_page().touch_note(x, y)
            self.temp_page.touch_note(x, y)
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
            for c, column in enumerate(grid):
                led_grid.append([self.get_led_status(x, c) for x in column])
            # Draw control sliders
            for y in range(8):
                # reset slider area (removes beat cursor)
                for x in range(16):
                    led_grid[x][y+8] = LED_BLANK
                for a in range(self.fire_chances[y]+1):
                    led_grid[7-a][y+8] = LED_ACTIVE
                led_grid[7-self.fire_chances[y]][y+8] = LED_SELECT
                led_grid[7][y+8] = LED_CURSOR
                for a in range(self.transpose_chances[y]):
                    led_grid[8+a][y+8] = LED_ACTIVE
                led_grid[8+self.transpose_chances[y]][y+8] = LED_SELECT
                led_grid[8][y+8] = LED_CURSOR
        elif state == 'ins_cfg':
            led_grid, cb_grid = generate_screen(dev_cfg_grid_defn, {'speed':int(self.speed), 'octave':int(self.octave), 'pages':[x.repeats for x in self.pages], 'curr_p_r': (self.curr_page_num, self.curr_rept_num)})
            self.cb_grid = cb_grid
            return led_grid
        return led_grid

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
        # Take control figures from new page, apply to controls
        notes = self.get_curr_page().note_grid
        for y in range(8, 16):
            for x in range(16):
                if notes[x][y] == NOTE_ON:
                    self.apply_control(x, y)
        self.apply_randomness()
        return

    def apply_randomness(self):
        '''Page has turned, apply randomness using source page onto temp page'''
        self.temp_page.note_grid = deepcopy(self.get_curr_page().note_grid)
        for x, beat in enumerate(self.temp_page.note_grid):  # For each beat
            for y, note in enumerate(beat[:8]):  # For each note in beat
                fire = self.calc_chance(self.fire_chances[y])
                if fire:
                    note = NOTE_ON if note == NOTE_OFF else NOTE_OFF
                    self.temp_page.note_grid[x][y] = note
                if note == NOTE_ON:
                    if self.calc_chance(self.transpose_chances[y]):
                        self.temp_page.note_grid[x][y+8] = NOTE_ON
                        self.temp_page.note_grid[x][y] = NOTE_OFF
        return

    def calc_chance(self, chance):
        '''chance is int between 0 and 8'''
        choices = [True] * chance + [False] * (20 - chance)
        c = choice(choices)
        return c

    def get_curr_notes(self):
        grid = self.temp_page.note_grid
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos][:8]]
        notes_on = [i for i, x in enumerate(beat_notes) if x == NOTE_ON]  # get list of cells that are on
        return notes_on
#
#     def output(self, old_notes, new_notes):
#         """Return all note-ons from the current beat, and all note-offs from the last"""
#         notes_off = [self.cell_to_midi(c) for c in old_notes]
#         notes_on = [self.cell_to_midi(c) for c in new_notes]
#         if self.sustain:
#             _notes_off = [n for n in notes_off if n not in notes_on]
#             _notes_on = [n for n in notes_on if n not in notes_off]
#             notes_off = _notes_off
#             notes_on = _notes_on
#         notes_off = [n for n in notes_off if n<128 and n>0]
#         notes_on = [n for n in notes_on if n<128 and n>0]
#         off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
#         on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
#         msgs = off_msgs + on_msgs
#         if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
#             for msg in msgs:
#                 self.mport.send(msg)
#
    def save(self):
        saved = {
          "pages": [p.save() for p in self.pages],
          "sustain": self.sustain,
          "random_rpt": self.random_pages,
          "fire_chances": self.fire_chances,
          "transpose_chances": self.transpose_chances,
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        self.sustain = saved["sustain"]
        self.random_pages = saved["random_rpt"]
        self.pages = []
        self.fire_chances = saved['fire_chances']
        self.transpose_chances = saved['transpose_chances']
        for p in saved["pages"]:
            page = Note_Grid(self.bars, self.height)
            page.load(p)
            self.pages.append(page)
        return


#     def clear_page(self):
#         self.get_curr_page().clear_page()
#         return
#
