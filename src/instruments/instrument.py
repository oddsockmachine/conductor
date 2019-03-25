#coding=utf-8
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALES, KEYS
import mido
from random import choice, random, randint

class Instrument(object):
    """docstring for Instrument."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Instrument, self).__init__()
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.type = "Generic Instrument"
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        self.height = 16
        self.width = 16
        self.prev_loc_beat = 0
        self.local_beat_position = 0  # Beat position due to instrument speed, which may be different to other instruments
        self.speed = speed  # Relative speed of this instrument compared to global clock
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
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, self.height)  # Function is cached for convenience

    # def cell_to_midi(self, cell):
    #     '''convert a cell height to a midi note based on key, scale, octave'''
    #     midi_note_num = self.note_converter[cell]
    #     return midi_note_num

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

    def get_curr_notes(self):
        grid = self.get_led_grid()
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

    #
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
    def calc_local_beat(self, global_beat):
        '''Calc local_beat_pos for this instrument'''
        div = self.get_beat_division()
        local_beat = int(global_beat / div) % self.width
        # logging.info("g{} d{} w{} l{}".format(global_beat, div, self.width, local_beat))
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
        notes_off = [n for n in notes_off if n<128 and n>0]
        notes_on = [n for n in notes_on if n<128 and n>0]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if self.mport:  # Allows us to not send messages if testing. TODO This could be mocked later
            for msg in msgs:
                self.mport.send(msg)

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
