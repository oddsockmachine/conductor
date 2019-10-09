# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from buses import midi_out_bus


class Marbles(Instrument):
    """Marbles
    https://mutable-instruments.net/modules/marbles/downloads/marbles_quickstart.pdf
    2 modes: controls mode, and visualization of buffers/notes

    The t generator produces random gates by generating a jittery master clock (which is output on t2) and deriving from it two streams of random gates which are output on t1 and t3.

    Clock comes in on step_beat
    Speed control divides or multiplies clock rate (beat_division)
    Control amount of randomness in the clock timing - perfectly stable, then simulating an instrumentalist lagging and catching up, then… complete chaos.
        Override calc_local_beat with a variable offset - offset from 0, to sine, to random

    Bias. Controls whether gates are more likely to occur on t1 or t3. Several methods are available for splitting the master clock into t1 and t3, selected by the button [E]:
    Random toin coss, with bias - or alternating, with bias (1,1,1,3,1,1,1,3)

    Consider length of note - static, random, part of generator? One every step/t2-trigger, or on until next note on t1/t3

    Deja Vu is a circular buffer, keeping track of previous states/choices
    At each step, choose whether to take value from a point in the buffer and move on, or generate new data, use it and store it in the buffer.
    Jitter offset from normal clock should also be saved in circular buffer
    DJV = 0: generate new data every tick.
    DJV = 0.5: always use circular buffer data
    DJV = 0.5>1: chance of jumping to new place within ciruclar buffer, using same data

    2 buttons to control whether DJV applies to t (ticks) or x (notes) or both

    Control for loop length: 1 - 16

    The X generator generates three independent random volt-ages output on X1, X2 and X3
    How to deal with 3 note outputs? 3 channels? Split by octave...
    Notes still constrained to scale - but what about drum/chromatic?
    Maybe selectable drum mode for each X output

    Probability Distribution control: from equal probability, to bell curve to very steep bell curve
    Distribution Bias: Skew distribution to high or low.
    Steppiness: necessary? Maybe replace with max step size between notes
    """

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Marbles, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Marbles"
        self.division = 2


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

    def save(self):
        saved = {
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        return
