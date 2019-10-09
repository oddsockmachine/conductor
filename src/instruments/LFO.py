# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from interfaces.lcd import lcd


class LFO(Instrument):
    """LFO
    - Sets ControlChange values
    - Multiple pages of sliders
    - Options for slew rate, transitions etc
    - Choose pages of 16 big sliders, 32 small sliders, etc"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(LFO, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "LFO"
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
        if x == 15:
            if y < c.H - self.max_pages:
                return
            self.curr_page_num = c.H-y-1
            return
        msg = self.get_curr_page().touch(x, y)
        msg.channel = self.ins_num
        self.mport.send(msg)
        return True

    def get_led_grid(self, state):
        grid = self.get_curr_page().get_led_grid()
        grid[15][15] = c.SLIDER_BODY
        grid[15][14] = c.SLIDER_BODY
        grid[15][13] = c.SLIDER_BODY
        grid[15][12] = c.SLIDER_BODY
        grid[15][c.H-self.curr_page_num-1] = c.SLIDER_TOP
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
