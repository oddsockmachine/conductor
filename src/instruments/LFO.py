# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from time import sleep
from math import radians, sin

class Oscillator(object):
    def __init__(self, speed):
        self.x = 0
        self.y = 0
        self.scale = 10 + speed # or speed
        self.uni_bi = 'uni'
        self.running = True # running, pause
        self.waveform = 'sine'
        self.pos = 0  # cc value, 0-127
        self.last_pos = 0

    def step(self):
        # TODO can calculate pos by interpolating time since last step
        if self.running:
            self.x = 0 if self.x >= 10 else self.x + 0.01
            self.y = sin(radians(self.x * self.scale))
            # c.debug(str(self.x) + str(self.y))
            self.pos = int(((self.y + 1) / 2) * 128)  # Convert -1..1 to 0..127
            if self.pos == self.last_pos:
                return None  # No noticable change in cc value
            self.last_pos = self.pos
            return self.pos
        return

    def pos_to_led_grid(self):
        return int(self.pos / 8)

class LFO(Instrument):
    """LFO
    Pages of 8x LFOs
    Visualize current position (dot or bar)
    At 100hz, probably possible to calculate LFO position each frame
    Choose waveform (sine, pulse, saw)
    Select an LFO, encoders set speed, division of bpm, play/pause,offset, nextpage
    """
    # TODO use separate timers for LFO, don't rely on beat sync
    # TODO ability to sync to multiple of bpm

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(LFO, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "LFO"
        self.height = 16
        self.width = 16
        self.counter = 0
        self.pages = []
        self.oscillators = [Oscillator(i) for i in range(8)]
        self.selected_osc = 0

    def run(self):
        while True:
            sleep(0.01)
            self.bump_counters()
        return

    def bump_counters(self):
        for osc in self.oscillators:
            cc = osc.step()
            if cc:
                pass
                # c.debug(str(cc))
                # TODO send CC msg to midi bus
        return

    def get_status(self):
        status = {
            # 'ins_num': self.ins_num+1,
            # 'ins_total': 16,
            # 'page_num': 0,
            # 'page_total': 0,
            # 'repeat_num': 0,
            # 'repeat_total': 0,
            # 'page_stats': {},
            # 'key': str(self.key),
            # 'scale': str(self.scale),
            # 'octave': str(self.octave),
            # 'type': self.type,
            # 'division': self.get_beat_division_str(),
            # 'random_rpt': False,
            # 'sustain': False,
        }
        return status

    def set_key(self, key):
        # Not implemented
        return

    def set_scale(self, scale):
        # Not implemented
        return

    def change_octave(self, up_down):
        # Not implemented
        return

    def get_curr_page(self):
        return self.pages[self.curr_page_num]

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        if not x % 2:
            return
        c.debug("!")
        osc = int((x-1)/2)
        # c.debug(osc)
        if y == 15:
            # Play/Pause button
            c.debug(f"play/pause {osc}")
            self.oscillators[osc].running = not self.oscillators[osc].running
        if y == 0:
            c.debug(f"selected {osc}")
            self.selected_osc = osc
            c.debug(self.selected_osc)
        return True

    def get_led_grid(self, state):
        grid = [
            [c.LED_BLANK for x in range(c.H)] for y in range(c.W)
        ]
        for i, osc in enumerate(self.oscillators):
            o1 = osc.pos_to_led_grid()
            grid[i*2][o1] = c.LED_ACTIVE
        for i in range(1, c.W, 2):
            # Red/Green play/pause buttons at y=0
            grid[i][15] = c.LED_BEAT
            # White select buttoons at y=15
            grid[i][0] = c.LED_CURSOR
        return grid

    def step_beat(self, global_beat):
        # c.debug("foo")
        return

    def output(self, old_notes, new_notes):
        return

    def save(self):
        saved = {
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        return

    def clear_page(self):
        self.get_curr_page().clear_page()
        return
