# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class Transformer(Instrument):
    """Transformer
    - Take a sequencer pattern, press one button to mutate by a set amount, another button to save the current state"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Transformer, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Transformer"
        self.height = 16
        self.width = 16
        self.local_beat_position = 0
        self.speed = speed
        self.droplet_velocities = [1 for n in range(self.width)]
        self.droplet_positions = [0 for n in range(self.width)]
        self.droplet_starts = [0 for n in range(self.width)]

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
        return

    def set_scale(self, scale):
        return

    def change_octave(self, up_down):
        return

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        return True

    def get_led_grid(self, state):
        page = [[c.LED_BLANK for y in range(self.height)] for x in range(self.width)]
        display = {
            0: c.DROPLET_STOPPED,
            1: c.DROPLET_SPLASH
        }
        for i in range(self.width):
            page[i][self.droplet_positions[i]] = display.get(self.droplet_positions[i], c.DROPLET_MOVING)
        return page

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        local
        new_notes = []
        # new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
        notes_off = [n for n in notes_off if n < 128 and n > 0]
        notes_on = [n for n in notes_on if n < 128 and n > 0]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if len(msgs) > 0:
            c.debug(msgs)
            midi_out_bus.put(msgs)

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
