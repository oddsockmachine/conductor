# coding=utf-8
from instruments.instrument import Instrument
import constants as c
from note_conversion import create_cell_to_midi_note_lookup, constrain_midi_notes
import mido
from buses import midi_out_bus


class Droplets(Instrument):
    """Droplets
    - Like Flin
    - Droplets fall vertically
    - Pitch is horizontal
    - Touch high up, droplet falls with high velocity
    - Touch low down, droplet falls with low velocity
    - Pitch is triggered when droplet reaches bottom
    - Touch above note to drag/extend it
    - Touch below note to catch/remove it
    - Add multiple drops per line?"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Droplets, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Droplets"
        self.height = 16
        self.width = 16
        self.local_beat_position = 0
        self.speed = speed  # Relative speed of this instrument compared to global clock
        self.droplet_velocities = [0 for n in range(self.width)]
        self.droplet_positions = [0 for n in range(self.width)]
        self.droplet_starts = [0 for n in range(self.width)]

    def restart(self):
        """Set all aspects of instrument back to starting state"""
        self.droplet_positions = [0 for n in range(self.width)]
        return

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

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''

        if y == 0:  # make droplet rest at 0
            self.droplet_positions[x] = 0
            self.droplet_starts[x] = 0
            self.droplet_velocities[x] = 0
        else:
            if self.droplet_velocities[x] == 0:  # droplet is resting, put it in play
                self.droplet_positions[x] = y
                self.droplet_starts[x] = y
                self.droplet_velocities[x] = 1
            else:  # droplet is falling, change its velocity
                self.droplet_velocities[x] = (y+1)/16
        return True

    def get_led_grid(self, state):
        page = [[c.LED_BLANK for y in range(self.height)] for x in range(self.width)]
        # display = {
        #     1: c.DROPLET_SPLASH
        # }
        for i in range(self.width):
            if self.droplet_velocities[i] == 0:
                page[i][int(self.droplet_positions[i])] = c.DROPLET_STOPPED
            elif self.droplet_positions[i] == 0:
                page[i][int(self.droplet_positions[i])] = c.DROPLET_SPLASH
            else:
                page[i][int(self.droplet_positions[i])] = c.DROPLET_MOVING
        return page

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        # TODO enable off-beat/smaller division steps
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            # Intermediate beat for this instrument, do nothing
            return
        self.local_beat_position = local
        new_notes = []
        for i in range(self.width):
            if self.droplet_velocities[i] == 0:
                continue  # Ignore any that we leave at 0, they're resting
            if self.droplet_positions[i] <= 0:
                self.droplet_positions[i] = self.droplet_starts[i]
            self.droplet_positions[i] -= self.droplet_velocities[i]
            if self.droplet_positions[i] <= 0:
                new_notes.append(i)
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

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
