from conductor import Conductor
from time import sleep
from constants import debug
from buses import actor_registry, bus_registry

class Supervisor(object):
    """docstring for Supercell."""

    def __init__(self):
        super(Supervisor, self).__init__()
        self.clock_bus = bus_registry.get('clock_bus')
        self.button_grid_bus = bus_registry.get('button_grid_bus')
        self.LED_grid_bus = bus_registry.get('LED_grid_bus')
        self.beat_clock_count = 0
        self.midi_clock_divider = 6
        self.conductor = Conductor()
        self.save_on_exit = False
        self.OLED_Screens = actor_registry.get_by_class_name('OLED_Screens')[0].proxy()
        self.OLED_Screens.text(0, ["hello"])
        self.OLED_Screens.text(1, ["world..."])
        for i in range(4):
            self.OLED_Screens.set_encoder_assignment(i, f"encoder {i}")
        self.keep_running = True

    def run(self):
        debug("Supervisor running...")
        self.draw()
        while self.keep_running:
            if not self.button_grid_bus.empty():
                # debug("button pressed")
                m = self.button_grid_bus.get()
                self.process_cmds(m)
                self.draw()
            if not self.clock_bus.empty():
                clock_tick = self.clock_bus.get()
                self.conductor.step_beat(clock_tick)
                self.draw()
            sleep(0.01)
        return

    def command_cb(self, m):
        self.process_cmds(m)
        return

    def get_cmds(self):
        if not self.button_grid_bus.empty():
            # debug("button pressed")
            m = self.button_grid_bus.get()
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
            self.conductor.step_beat(1)
        elif m['cmd'] == 'note':
            self.conductor.touch_note(m['x'], m['y'])
        elif m['cmd'] == 'encoder':
            self.conductor.touch_encoder(id=m['id'], action=m['action'])
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
        screens = self.OLED_Screens.get_text().get()
        self.LED_grid_bus.put((status, led_grid, screens))