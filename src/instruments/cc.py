# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from interfaces.lcd import lcd


class SliderBank(object):
    """docstring for SliderBank."""

    def __init__(self, offset):
        super(SliderBank, self).__init__()
        self.sliders = [Slider(offset+x) for x in range(c.W-1)]

    def touch(self, x, y):
        return self.sliders[x].set(y)

    def get_led_grid(self):
        leds = [[c.LED_BLANK for y in range(c.H)] for x in range(c.W)]
        for i, s in enumerate(self.sliders):  # sliders along x axis
            leds[i][s.value] = c.SLIDER_TOP
            for j in range(s.value):
                leds[i][j] = c.SLIDER_BODY
        return leds


class Slider(object):
    """docstring for Slider."""

    def __init__(self, id):
        super(Slider, self).__init__()
        self.height = c.H
        self.value = 0
        self.options = {}
        self.cc_num = id

    def get_cc(self):
        return int(self.value * (128/(self.height-1)))

    def set(self, value):
        if value > self.height:
            return  # Not possible
        self.value = value
        cc = self.get_cc()
        c.logging.info("CC{} = {}, {}".format(self.cc_num, self.value, cc))
        lcd.flash("CC{} = {}, {}".format(self.cc_num, self.value, cc))
        msg = mido.Message('control_change', value=cc, control=self.cc_num, channel=0)
        return msg


class CC(Instrument):
    """CC
    - Sets ControlChange values
    - Multiple pages of sliders
    - Options for slew rate, transitions etc
    - Choose pages of 16 big sliders, 32 small sliders, etc"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(CC, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "CC"
        self.height = 16
        self.width = 16
        self.curr_page_num = 0
        self.max_pages = 4
        self.pages = []
        for i in range(self.max_pages):
            self.pages.append(SliderBank(len(self.pages*15)))
        #     self.pages.append(SliderBank(0))
        # self.pages.append(SliderBank(15))
        # self.pages.append(SliderBank(30))
        # self.pages.append(SliderBank(45))

    def add_page(self, type):
        self.pages.append(SliderBank(len(self.pages*15)))

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
        return True

    def get_led_grid(self, state):
        grid = [
            [c.LED_BLANK for x in range(c.H)] for y in range(c.W)
        ]
        return grid

    def step_beat(self, global_beat):
        return

    def output(self, old_notes, new_notes):
        return

    def save(self):
        saved = {
          "values": [[v.value for v in p.sliders] for p in self.pages]
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        values = saved["values"]
        self.pages = []
        for p in values:
            sb = SliderBank(len(self.pages*15))
            for i, v in enumerate(p):
                sb.sliders[i].value = v
            self.pages.append(sb)
        return

    def clear_page(self):
        self.get_curr_page().clear_page()
        return
