from controller import Controller
from constants import *
from time import sleep, time
from datetime import datetime
from json import dump, load

class Supercell(object):
    """docstring for Supercell."""
    def __init__(self, display, mport, mportin, saved_set=None):
        super(Supercell, self).__init__()
        self.mport = mport
        self.mportin = mportin
        self.beatclockcount = 0
        self.mportin.callback = self.process_incoming_midi()
        # Check for loading previous set
        if saved_set:
            with open(saved_set, 'r') as saved_file:
                saved_data = load(saved_file)
            self.controller = Controller(mport, saved=saved_data)
        else:
            self.controller = Controller(mport, saved=None)
        self.last = time()
        self.display = display
        self.display.command_cb = self.command_cb
        self.save_on_exit = False

    def run(self):
        self.draw()
        while True:
            self.get_cmds()
            sleep(0.1)  # TODO REMOVE TODO
            # self.controller.step_beat()  # TODO REMOVE TODO
            self.draw()  # TODO REMOVE TODO
        pass

    def process_incoming_midi(self):
        def _process_incoming_midi(message, timestamp=0):
            '''Check for incoming midi messages and categorize so we can do something with them'''
            tick = False
            notes = []
            if message.type == "clock":
                tick = self.process_midi_tick()
                if tick:
                    self.controller.step_beat()
                    # self.draw()
            if message.type == "note_on":
                self.controller.add_notes_from_midi([message.note])
        return _process_incoming_midi

    def command_cb(self, m):
        self.process_cmds(m)
        return

    def get_cmds(self):
        m = self.display.get_cmds()
        self.process_cmds(m)

    def process_cmds(self, m):
        if m['cmd'] == None:
            return None
        if m['cmd'] == 'quit':
            if self.save_on_exit:
                self.save()
            exit()
        elif m['cmd'] == 'toggle_save':
            self.save_on_exit = not self.save_on_exit
            logging.info(self.save_on_exit)
        elif m['cmd'] == 'save':
            self.save()
        elif m['cmd'] == 'step_beat':
            self.controller.step_beat()
        elif m['cmd'] == 'clear_page':
            self.controller.clear_page()
        elif m['cmd'] == 'cycle_key':
            self.controller.cycle_key(m['dir'])
        elif m['cmd'] == 'cycle_scale':
            self.controller.cycle_scale(m['dir'])
        elif m['cmd'] == 'swap_drum_inst':
            self.controller.swap_drum_inst()
        elif m['cmd'] == 'change_octave':
            self.controller.change_octave(m['dir'])
        elif m['cmd'] == 'note':
            self.controller.touch_note(m['x'], m['y'])
        elif m['cmd'] == 'ins':
            self.controller.current_visible_instrument = m['ins']
        elif m['cmd'] == 'inc_rep':
            self.controller.inc_rep(m['page'])
        elif m['cmd'] == 'dec_rep':
            self.controller.dec_rep(m['page'])
        elif m['cmd'] == 'add_page':
            self.controller.add_page()
        elif m['cmd'] == 'change_division':
            self.controller.change_division(m['div'])
        elif m['cmd'] == 'random_rpt':
            self.controller.get_curr_instrument().random_pages = False if self.controller.get_curr_instrument().random_pages else True
        elif m['cmd'] == 'sustain':
            self.controller.get_curr_instrument().sustain = False if self.controller.get_curr_instrument().sustain else True
        elif m['cmd'] == 'chaos':
            self.controller.get_curr_instrument().update_chaos(m['dir'])
        elif m['cmd'] == 'z_mode':
            self.controller.toggle_z_mode()
        return

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        self.beatclockcount += 1
        if self.beatclockcount >= 3:
            self.beatclockcount %= 3
            return True
        return False

    def draw(self):
        status = self.controller.get_status()
        led_grid = self.controller.get_led_grid()
        self.display.draw_all(status, led_grid)

    def save(self):
        print("Saving current grid to {}.cell".format(datetime.now()))
        filename = './saved/' + str(datetime.now()).split('.')[0] + '.json'
        with open(filename, 'w') as savefile:
            saved = self.controller.save()
            dump(saved, savefile)
