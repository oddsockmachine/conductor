# coding=utf-8
import constants as c
from instruments import instrument_lookup
from note_conversion import SCALE_INTERVALS, KEYS
from save_utils import get_all_set_file_numbers, filenum_from_touch, validate_filenum, load_filenum, save_filenum
from screens import generate_screen, gbl_cfg_grid_defn, get_cb_from_touch
from interfaces.lcd import lcd


class Conductor(object):
    """docstring for Conductor."""

    def __init__(self, key="e", scale="pentatonic_maj", octave=2, bars=int(c.W/4), height=c.H):
        super(Conductor, self).__init__()
        self.mport = None
        self.key = key
        self.states = 'play save load ins_cfg gbl_cfg display'.split()  # Valid states for the display(s)
        self.beat_position = 0
        self.height = c.H
        self.width = bars*4
        self.bars = bars
        self.max_beat_division = 32
        self.scale = scale
        self.octave = octave  # Starting octave
        self.instruments = [instrument_lookup(5)(ins_num=0, **self.instrument_ctx())]
        self.instruments[0].start()
        # for x in range(4):
        #     self.instruments.append(instrument_lookup(4)(ins_num=x+3, **self.instrument_ctx()))
        # self.instruments.append(instrument_lookup(9)(ins_num=8, **self.instrument_ctx()))
        # self.instruments.append(instrument_lookup(8)(ins_num=9, **self.instrument_ctx()))
        # self.instruments.append(instrument_lookup('Octopus')(ins_num=10, **self.instrument_ctx()))
        #
        # self.instruments.append(instrument_lookup(7)(ins_num=14, **self.instrument_ctx()))
        # self.instruments.append(instrument_lookup(5)(ins_num=15, **self.instrument_ctx()))
        self.current_visible_instrument_num = 0
        self.current_state = 'load'  # Current state to be shown on display(s)
        lcd.flash("Conductor started")
        return

    def instrument_ctx(self):
        return {
            'mport': self.mport,
            'key': self.key,
            'scale': self.scale,
            'octave': self.octave,
            'speed': 1
        }

    def ins_cfg_state(self):
        if self.current_state == 'ins_cfg':
            self.current_state = 'play'
        else:
            self.current_state = 'ins_cfg'
        return

    def gbl_cfg_state(self):
        if self.current_state == 'gbl_cfg':
            self.current_state = 'play'
        else:
            self.current_state = 'gbl_cfg'
        return

    def save_state(self):
        if self.current_state == 'save':
            self.current_state = 'play'
        else:
            self.current_state = 'save'
        return

    def load_state(self):
        if self.current_state == 'load':
            self.current_state = 'play'
        else:
            self.current_state = 'load'
        return

    def get_led_grid(self):
        '''Get led status types for all cells of the grid, to be drawn by the display'''
        display_func_name = self.current_state + '_screen'
        self.__getattribute__(display_func_name)
        display_func = getattr(self, display_func_name)
        return display_func()

    def play_screen(self):
        led_grid = self.get_curr_instrument().get_led_grid(self.current_state)
        return led_grid

    def gbl_cfg_screen(self):
        led_grid, cb_grid = generate_screen(gbl_cfg_grid_defn, {
            'scale_chars': c.SCALE_CHARS[self.scale],
            'key': self.key+' ',
            'num_ins': self.get_total_instrument_num(),
            'curr_ins': self.get_curr_instrument_num()-1})
        self.gbl_cfg_cb_grid = cb_grid
        return led_grid
        # return create_gbl_cfg_grid(range(len(self.instruments)), self.key, self.scale)

    def ins_cfg_screen(self):
        led_grid = self.get_curr_instrument().get_led_grid('ins_cfg')
        return led_grid

    def load_screen(self):
        led_grid = []
        for x in range(16):
            led_grid.append([c.LED_BLANK for y in range(16)])
        files = get_all_set_file_numbers()
        for f in files:
            if f > 254:  # TODO add a slot for empty/new
                continue
            if f == 0:
                continue
            x = int(f / 16)
            y = int(f % 16)
            led_grid[y][15-x] = c.LED_ACTIVE
        led_grid[0][15] = c.LED_CURSOR
        return led_grid

    def save_screen(self):
        return self.load_screen()

    def add_instrument(self, type):
        if len(self.instruments) == 16:
            return
        ins_type = instrument_lookup(type)
        new_ins = ins_type(ins_num=len(self.instruments), **self.instrument_ctx())
        new_ins.start()
        self.instruments.append(new_ins)
        return

    def get_status(self):
        status = self.get_curr_instrument().get_status()
        return status

    def step_beat(self, tick_type):
        self.beat_position += 1
        self.beat_position %= self.width * self.max_beat_division
        for ins in self.instruments:
            # ins.step_beat()#self.beat_position)
            ins.step_beat(self.beat_position)
        pass

    def restart(self):
        """Set all instruments back to starting state, beat 0, page 0"""
        # TODO
        for ins in self.instruments:
            ins.restart()
        return

    def save(self, filenum=None):
        data = {
            "height": 16,
            "width": 16,
            "instruments": [i.save() for i in self.instruments]
        }
        save_filenum(data, filenum)

    def load(self, saved):
        self.height = saved['height']
        self.width = saved['width']
        self.scale = saved['instruments'][0]['scale']
        self.octave = saved['instruments'][0]['octave']
        self.key = saved['instruments'][0]['key']
        self.instruments = []  # Loading, so clear away all old instruments
        for i in range(len(saved['instruments'])):
            self.add_instrument(saved['instruments'][i]['type'])
            self.instruments[i].load(saved['instruments'][i])
        self.current_state = 'gbl_cfg'
        return

    def touch_note(self, x, y):
        if self.current_state == 'play':
            self.get_curr_instrument().touch_note(self.current_state, x, y)
        elif self.current_state == 'load':
            c.logging.info("loading")
            filenum = filenum_from_touch(x, y)
            if not validate_filenum(filenum):
                return
            if filenum == 1:
                return
            self.load(load_filenum(filenum))
            c.logging.info("loaded {}".format(filenum))
            self.current_state == 'play'
        elif self.current_state == 'save':
            c.logging.info("Saving {} {}".format(x, y))
            filenum = filenum_from_touch(x, y)
            if validate_filenum(filenum):
                c.logging.info("already exists, ignoring")
                self.current_state == 'play'
                return  # don't overwrite existing files
            self.save(filenum)
            c.logging.info("saved")
            self.current_state == 'play'
        elif self.current_state == 'gbl_cfg':
            cb_text, _x, _y = get_cb_from_touch(self.gbl_cfg_cb_grid, x, y)  # Find which area was touched
            if not cb_text:
                return
            cb_func = self.__getattribute__('cb_' + cb_text)  # Lookup the relevant conductor function
            cb_func(_x, _y)  # call it, passing it x/y args (which may not be needed)
        elif self.current_state == 'ins_cfg':
            self.get_curr_instrument().touch_note(self.current_state, x, y)
            # cb = get_cb_from_touch(get_ins_cfg_cb_grid(self.get_curr_instrument_num()), x, y)
        return

    # ##### CALLBACK METHODS ######

    def cb_reset(self, x, y):
        self.beat_position = 0
        for i in self.instruments:
            i.local_beat_position = 0
            try:
                i.curr_page_num = 0
                i.curr_rept_num = 0
            except Exception as e:
                str(e)
                pass
            if i.type == 'Droplets':
                i.droplet_positions = [d for d in i.droplet_starts]
        self.current_state = 'play'
        lcd.flash("Reset all")
        return

    def cb_scale_inc(self, x, y):
        self.cycle_scale(1)
        return

    def cb_scale_dec(self, x, y):
        self.cycle_scale(-1)
        return

    def cb_key_inc(self, x, y):
        self.cycle_key(1)
        return

    def cb_key_dec(self, x, y):
        self.cycle_key(-1)
        return

    def cb_load(self, x, y):
        self.current_state = 'load'
        lcd.flash("Select load")
        return

    def cb_save(self, x, y):
        self.current_state = 'save'
        lcd.flash("Select save file")
        return

    def cb_instrument_del(self, x, y):
        if len(self.instruments) == 1:
            return
        ins_num = self.get_curr_instrument_num() - 1
        # c.logging.info(f"deleting instrument num {ins_num}")
        # lcd.flash(f"deleting instrument num {ins_num}")
        # c.logging.info(f"total instruments before {len(self.instruments)}")
        self.instruments.pop(ins_num)
        # c.logging.info(f"total instruments after {len(self.instruments)}")
        for i, ins in enumerate(self.instruments):
            ins.ins_num = i
        return

    def cb_instrument_sel(self, x, y):
        if int(y) < self.get_total_instrument_num():
            self.set_curr_instrument(int(y))
            self.current_state = 'play'
        lcd.flash("Selected {}".format(self.get_curr_instrument().type))
        return

    def cb_instrument_type(self, x, y):
        if self.get_total_instrument_num() >= 16:
            return
        ins = instrument_lookup(y+1)  # +1 because base class isn't playable
        new_ins = ins(ins_num=self.get_total_instrument_num(), **self.instrument_ctx())
        new_ins.start()
        self.instruments.append(new_ins)
        lcd.flash("Added {}".format(self.instruments[~0].type))

    # ###### GETTERS/SETTERS ######

    def get_curr_instrument(self):
        return self.instruments[self.current_visible_instrument_num]

    def set_curr_instrument(self, num):
        self.current_visible_instrument_num = num
        self.current_state = 'play'

    def get_curr_instrument_num(self):
        return self.current_visible_instrument_num + 1

    def get_total_instrument_num(self):
        return len(self.instruments)

    def cycle_key(self, up_down):
        '''Find current key in master list, move on to prev/next key, set in all instruments'''
        curr_key = KEYS.index(self.key)
        new_key = (curr_key + up_down) % len(KEYS)
        self.key = KEYS[new_key]
        for i in self.instruments:
            i.set_key(self.key)
            c.logging.info(i.type)
        # c.logging.info(f"Scale {self.key}")
        lcd.flash("Key {}".format(self.key))
        return

    def cycle_scale(self, up_down):
        '''Find current scale in master list, move on to prev/next scale, set in all instruments'''
        curr_scale = list(SCALE_INTERVALS.keys()).index(self.scale)
        new_scale = (curr_scale + up_down) % len(SCALE_INTERVALS.keys())
        self.scale = list(SCALE_INTERVALS.keys())[new_scale]
        for i in self.instruments:
            i.set_scale(self.scale)
            c.logging.info(i.type)
        # c.logging.info(f"Scale {self.scale}")
        lcd.flash("Scale {}".format(self.scale))
        return

    # ##### CONTROL PASSTHROUGH METHODS ######

    def change_division(self, up_down):
        self.get_curr_instrument().change_division(up_down)
        return

    def change_octave(self, up_down):
        self.get_curr_instrument().change_octave(up_down)
        return

    def inc_rep(self, page):
        self.get_curr_instrument().inc_page_repeats(page)
        return

    def dec_rep(self, page):
        self.get_curr_instrument().dec_page_repeats(page)
        return

    def add_page(self):
        self.get_curr_instrument().add_page()
        return

    def clear_page(self):
        self.get_curr_instrument().clear_page()
        return
