# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import mido
from screens import generate_screen, cc_cfg_grid_defn, get_cb_from_touch


class SliderPage(object):
    """docstring for SliderPage."""

    def __init__(self, type, offset):
        super(SliderPage, self).__init__()
        self.sliders = [Slider(c.H, offset+x) for x in range(c.W)]

    def touch(self, x, y):
        self.sliders[x].touch(y)

    def get_led_grid(self):
        leds = [[c.LED_BLANK for y in range(c.H)] for x in range(c.W)]
        for i, s in enumerate(self.sliders):  # sliders along x axis
            leds[i][s.value] = c.SLIDER_TOP
            for j in range(s.value):
                leds[i][j] = c.SLIDER_BODY
        return leds


class Slider(object):
    """docstring for Slider."""

    def __init__(self, height, id):
        super(Slider, self).__init__()
        self.height = height
        self.value = 0
        self.options = {}
        self.cc_num = id

    def get_cc(self):
        return self.value * (128/self.height)

    def set(self, value):
        if value > self.height:
            return  # Not possible
        self.value = value


class CC(Instrument):
    """CC
    - Sets ControlChange values
    - Multiple pages of sliders
    - Options for slew rate, transitions etc
    - Choose pages of 16 big sliders, 32 small sliders, etc"""

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(CC, self).__init__(ins_num, mport, key, scale, octave, speed)
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.type = "CC"
        self.height = 16
        self.width = 16
        self.curr_page_num = 0
        self.pages = []
        self.pages.append(SliderPage('A', 0))
        self.pages.append(SliderPage('A', 16))
        self.pages.append(SliderPage('B', 32))
        self.pages.append(SliderPage('A', 64))
        self.pages.append(SliderPage('A', 80))
        self.pages.append(SliderPage('B', 96))

    def add_page(self, type):
        self.pages.append(SliderPage(type))

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
        if state == 'play':
            self.get_curr_page().touch(x, y)
        elif state == 'ins_cfg':
            cb_text, _x, _y = get_cb_from_touch(self.cb_grid, x, y)
            c.logging.info(cb_text)
            if not cb_text:
                return
            cb_func = self.__getattribute__('cb_' + cb_text)  # Lookup the relevant conductor function
            cb_func(_x, _y)  # call it, passing it x/y args (which may not be needed)
            return True

        return True

    def get_led_grid(self, state):
        if state == 'play':
            return self.get_curr_page().get_led_grid()
        elif state == 'ins_cfg':
            led_grid, cb_grid = generate_screen(cc_cfg_grid_defn, {
                'pages': [1 for x in self.pages],
                'curr_p_r':  (self.curr_page_num, 0)
                })
            self.cb_grid = cb_grid
            return led_grid
        return led_grid

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
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
