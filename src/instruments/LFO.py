# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from time import sleep
from math import radians, sin

class Oscillator(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 360  # or speed
        self.uni_bi = 'uni'
        self.state = 'running' # running, pause
        self.waveform = 'sine'
    
    def step(self):
        # TODO can calculate pos by interpolating time since last step
        if self.state == 'running':
            self.x = 0 if self.x >= 1 else self.x + 0.01
            self.y = sin(radians(self.x * self.scale))
            c.debug(str(self.x) + str(self.y))
            # If uni, add 0.5
            # Check old pos, to decide whether to send midi cc
        return

    def pos_to_led_grid(self):
        return int(self.y * c.H)

class LFO(Instrument):
    """LFO
    Pages of 8x LFOs
    Visualize current position (dot or bar)
    Unipolar (0-1, all green) or bipolar (-1 to 1, red/green)
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
        self.oscillators = [Oscillator() for i in range(2)]
    
    def run(self):
        while True:
            sleep(0.01)
            self.bump_counters()
        return

    def bump_counters(self):
        for osc in self.oscillators:
            osc.step()
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
        # if x == 15:
        #     if y < c.H - self.max_pages:
        #         return
        #     self.curr_page_num = c.H-y-1
        #     return
        # msg = self.get_curr_page().touch(x, y)
        # msg.channel = self.ins_num
        # self.mport.send(msg)
        return True

    def get_led_grid(self, state):
        c.debug("grid")
        grid = [
            [c.LED_BLANK for x in range(c.H)] for y in range(c.W)
        ]
        o1 = self.oscillators[0].pos_to_led_grid()
        grid[3][o1] = c.LED_ACTIVE
        # grid[15][15] = c.SLIDER_BODY
        # grid[15][14] = c.SLIDER_BODY
        # grid[15][13] = c.SLIDER_BODY
        # grid[15][12] = c.SLIDER_BODY
        # grid[15][c.H-self.curr_page_num-1] = c.SLIDER_TOP
        return grid

    def step_beat(self, global_beat):
        c.debug("foo")
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
