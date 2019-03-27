#coding=utf-8
from instruments.instrument import Instrument
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, SCALE_INTERVALS, KEYS
import mido
from random import choice, random, randint

class Droplets(Instrument):
    """docstring for Droplets."""
    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Droplets, self).__init__(ins_num, mport, key, scale, octave, speed)
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.type = "Droplets"
        # self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        # self.mport = mport
        # # logging.info(mport)
        self.height = 16
        # self.bars = bars #min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = 16
        # self.curr_page_num = 0
        # self.curr_rept_num = 0
        # self.prev_loc_beat = 0
        self.local_beat_position = 0  # Beat position due to instrument speed, which may be different to other instruments
        self.speed = speed  # Relative speed of this instrument compared to global clock
        # self.isdrum = False  # Chromatic instrument for drum tracks
        # self.random_pages = False  #  Pick page at random
        # self.sustain = True  # Don't retrigger notes if this is True
        # self.chaos = 0.0  # Add some randomness to notes
        # self.page = Note_Grid(self.bars, self.height)
        self.droplet_velocities = [1 for n in range(self.width)]
        self.droplet_positions = [0 for n in range(self.width)]
        self.droplet_starts = [0 for n in range(self.width)]
        # if key not in KEYS:
        #     print('Requested key {} not known'.format(key))
        #     exit()
        # self.key = key
        # if scale not in SCALES.keys():
        #     print('Requested scale {} not known'.format(scale))
        #     exit()
        # self.scale = scale
        # self.octave = octave  # Starting octave
        # self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        # self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, height)  # Function is cached for convenience

    def get_status(self):
        status = {
            'ins_num': self.ins_num+1,
            'ins_total': 16,
            'page_num': 0,
            'page_total': 0,
            'repeat_num': 0,
            'repeat_total': 0,
            'page_stats': {},
            'key': str(self.key),
            'scale': str(self.scale),
            'octave': str(self.octave),
            'type': self.type,
            'division': self.get_beat_division_str(),
            'random_rpt': False,
            'sustain': False,
        }
        return status


    def set_key(self, key):
        self.key = key
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def set_scale(self, scale):
        self.scale = scale
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def change_octave(self, up_down):
        self.octave = up_down  #TODO handle up and down as well as octave number
        # self.octave = (self.octave + up_down) % 7
        # Converter is a cached lookup, we need to regenerate it
        self.note_converter = create_cell_to_midi_note_lookup(self.scale, self.octave, self.key, self.height)
        return True

    def cell_to_midi(self, cell):
        '''convert a cell height to a midi note based on key, scale, octave'''
        midi_note_num = self.note_converter[cell]
        return midi_note_num

    def touch_note(self, x, y):
        '''touch the x/y cell on the current page'''
        # if y < 4:
        #     self.droplet_velocities[x] = y
        # else:
        self.droplet_positions[x] = y
        self.droplet_starts[x] = y
        return True
    #
    # def get_notes_from_curr_beat(self):
    #     # self.get_curr_page().get_notes_from_beat(self.local_beat_position)
    #     return

    # def get_curr_page_leds(self):
    #     return

    def get_led_grid(self, state):
        page = [[LED_BLANK for y in range(self.height)] for x in range(self.width)]
        display = {
            0: DROPLET_STOPPED,
            1: DROPLET_SPLASH
        }
        for i in range(self.width):
            page[i][self.droplet_positions[i]] = display.get(self.droplet_positions[i], DROPLET_MOVING)
        return page

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            # Intermediate beat for this instrument, do nothing
            return
        self.local_beat_position = local
        # if self.is_page_end():
        #     self.advance_page()
        new_notes = []
        for i in range(self.width):
            if self.droplet_positions[i] == 0:
                continue  # Ignore any that we leave at 0, they're resting
            self.droplet_positions[i] -= self.droplet_velocities[i]
            if self.droplet_positions[i] <= 0:
                new_notes.append(i)
                self.droplet_positions[i] = self.droplet_starts[i]
        # new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def calc_local_beat(self, global_beat):
        '''Calc local_beat_pos for this instrument'''
        div = self.get_beat_division()
        local_beat = int(global_beat / div) % self.width
        # logging.info("g{} d{} w{} l{}".format(global_beat, div, self.width, local_beat))
        return local_beat

    def has_beat_changed(self, local_beat):
        if self.prev_loc_beat != local_beat:
            self.prev_loc_beat = local_beat
            return True
        self.prev_loc_beat = local_beat
        return False

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

    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
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
          "droplet_velocities": self.droplet_velocities,
          "droplet_positions": self.droplet_positions,
          "droplet_starts": self.droplet_starts,
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        self.droplet_velocities = saved["droplet_velocities"]
        self.droplet_positions = saved["droplet_positions"]
        self.droplet_starts = saved["droplet_starts"]
        return

    def clear_page(self):
        self.get_curr_page().clear_page()
        return
