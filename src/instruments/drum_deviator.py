#coding=utf-8
from instruments.instrument import Instrument
from instruments.drum_machine import DrumMachine
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALES, KEYS
import mido
from random import choice, random, randint

class DrumDeviator(DrumMachine):
    """docstring for DrumDeviator."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(DrumDeviator, self).__init__(ins_num, mport, key, scale, octave, speed)
        if not isinstance(ins_num, int):
            print("DrumDeviator num {} must be an int".format(ins_num))
            exit()
        self.type = "Drum Deviator"
#         self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
#         self.mport = mport
#         # logging.info(mport)
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

    def touch_note(self, x, y):
        '''touch the x/y cell on the current page - either a control, or a note'''
        # Is touch control or note?
        if y >= 8:
            # Control TODO
            y-=8
            if x < 8: # Fire chances
                self.fire_chances[y] = 7 - x

            else:  # Transpose chances
                self.transpose_chances[y] = x - 8
            return True
        else:
            # Apply touch to current temp page and source page
            self.get_curr_page().touch_note(x, y)
            self.temp_page.touch_note(x, y)
        return True

    def get_led_grid(self):
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
#
#     def get_next_page_num(self):
#         '''Return the number of the next page that has a positive number of repeats
#         or return a random page if wanted'''
#         if self.random_pages:
#             # Create a distribution of the pages and their repeats, pick one at random
#             dist = []
#             for index, page in enumerate(self.pages):
#                 for r in range(page.repeats):
#                     dist.append(index)
#             next_page_num = choice(dist)
#             return next_page_num
#         for i in range(1, len(self.pages)):
#             # Look through all the upcoming pages
#             next_page_num = (self.curr_page_num + i) % len(self.pages)
#             rpts = self.pages[next_page_num].repeats
#             # logging.info("i{} p{} r{}".format(i, next_page_num, rpts))
#             if rpts > 0:  # This one's good, return it
#                 return next_page_num
#         # All pages including curr_page are zero repeats, just stick with this one
#         return self.curr_page_num
#
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
        self.apply_randomness()
        return

    def apply_randomness(self):
        '''Page has turned, apply randomness using source page onto temp page'''
        source_page = self.get_curr_page().note_grid
        for x in range(self.width):  # Copy notes from source to temp
            self.temp_page.note_grid[x] = source_page[x]
        for x in range(self.width):
            for y in range(8):
                self.temp_page.note_grid[x][y+8] = self.temp_page.note_grid[x][y]
        return
#
    def get_curr_notes(self):
        grid = self.temp_page.note_grid
        beat_pos = self.local_beat_position
        beat_notes = [n for n in grid[beat_pos]]
        # if self.chaos > 0:  # If using chaos, switch up some notes
        #     if beat_notes.count(NOTE_ON) > 0:  # Only if there are any notes in use
        #         if random() < self.chaos:
        #             rand_note = randint(0, self.height-1)
        #             beat_notes[rand_note] = NOTE_ON if beat_notes[rand_note] != NOTE_ON else NOTE_OFF
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
#     def save(self):
#         saved = {
#           "Octave": self.octave,
#           "Key": self.key,
#           "Scale": self.scale,
#           "Pages": [p.save() for p in self.pages],
#           "Speed": self.speed,
#           "IsDrum": self.isdrum,
#           "Sustain": self.sustain,
#           "Chaos": self.chaos,
#           "RandomRpt": self.random_pages,
#         }
#         return saved
#
#     def load(self, saved):
#         self.octave = saved["Octave"]
#         self.key = saved["Key"]
#         self.scale = saved["Scale"]
#         self.speed = saved["Speed"]
#         self.isdrum = saved["IsDrum"]
#         self.sustain = saved["Sustain"]
#         self.chaos = saved["Chaos"]
#         self.random_pages = saved["RandomRpt"]
#         self.pages = []
#         for p in saved["Pages"]:
#             page = Note_Grid(self.bars, self.height)
#             print(p)
#             page.load(p)
#             self.pages.append(page)
#         return
#
#     def clear_page(self):
#         self.get_curr_page().clear_page()
#         return
#
