from conductor import Conductor
from time import sleep, time



class Supercell(object):
    """docstring for Supercell."""

    def __init__(self, display, mport, mportin, saved_set=None):
        super(Supercell, self).__init__()
        self.mport = mport
        self.mportin = mportin
        self.beat_clock_count = 0
        self.midi_clock_divider = 7
        self.mportin.callback = self.process_incoming_midi()
        self.conductor = Conductor(mport)
        self.last = time()
        self.display = display
        self.display.command_cb = self.command_cb
        self.save_on_exit = False
        self.CLOCK = 0

    def run(self):
        print("Running...")
        self.draw()
        while True:
            self.CLOCK += 1
            if (self.CLOCK % 10) == 0:
                self.conductor.step_beat()
            self.get_cmds()
            sleep(0.1)  # TODO REMOVE TODO
            # self.conductor.step_beat()  # TODO REMOVE TODO
            self.draw()  # TODO REMOVE TODO
        pass

    def process_incoming_midi(self):
        def _process_incoming_midi(message, timestamp=0):
            '''Check for incoming midi messages and categorize so we can do something with them'''
            tick = False
            # notes = []
            if message.type == "clock":
                tick = self.process_midi_tick()
                if tick:
                    self.conductor.step_beat()
                    # self.draw()
        return _process_incoming_midi

    def command_cb(self, m):
        self.process_cmds(m)
        return

    def get_cmds(self):
        m = self.display.get_cmds()
        self.process_cmds(m)

    def process_cmds(self, m):
        if m['cmd'] is None:
            return None
        if m['cmd'] == 'quit':
            if self.save_on_exit:
                self.conductor.save()
            exit()
        elif m['cmd'] == 'toggle_save':
            self.save_on_exit = not self.save_on_exit
        elif m['cmd'] == 'CONFIG_A':
            self.conductor.gbl_cfg_state()
        elif m['cmd'] == 'CONFIG_B':
            self.conductor.ins_cfg_state()
        elif m['cmd'] == 'step_beat':
            self.conductor.step_beat()
        elif m['cmd'] == 'note':
            self.conductor.touch_note(m['x'], m['y'])
        return

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        self.beat_clock_count += 1
        if self.beat_clock_count >= self.midi_clock_divider:
            self.beat_clock_count %= self.midi_clock_divider
            return True
        return False

    def draw(self):
        status = self.conductor.get_status()
        led_grid = self.conductor.get_led_grid()
        self.display.draw_all(status, led_grid)
