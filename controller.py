from sequencer import Sequencer
from constants import *
from time import sleep, time
from datetime import datetime
import mido
from json import dump, load
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--set", help="Filename of previous set to load", type=str)
parser.add_argument("--hw",  help="Use real hardware", type=bool)
args = parser.parse_args()
print(args)

class Controller(object):
    """docstring for Controller."""
    def __init__(self, display, mport, mportin):
        super(Controller, self).__init__()
        self.mport = mport
        self.mportin = mportin
        self.mportin.callback = self.process_incoming_midi()
        # Check for loading previous set
        if args.set:
            saved = args.set
            with open(saved, 'r') as saved_file:
                saved_set = load(saved_file)
            self.sequencer = Sequencer(mport, saved=saved_set)
        else:
            self.sequencer = Sequencer(mport, saved=None)
        self.last = time()
        self.display = display
        self.display.command_cb = self.command_cb
        self.beatclockcount = 0
        self.save_on_exit = False

    def run(self):
        self.draw()
        while True:
            self.get_cmds()
            sleep(0.3)  # TODO REMOVE TODO
            self.sequencer.step_beat()  # TODO REMOVE TODO
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
                    self.sequencer.step_beat()
                    self.draw()
            if message.type == "note_on":
                self.sequencer.add_notes_from_midi([message.note])
        return _process_incoming_midi

    def command_cb(self, m):
        self.process_cmds(m)
        # if m['cmd'] == 'note':
        #     self.sequencer.touch_note(m['x'], m['y'])
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
            self.sequencer.step_beat()
        elif m['cmd'] == 'clear_page':
            self.sequencer.clear_page()
        elif m['cmd'] == 'cycle_key':
            self.sequencer.cycle_key(m['dir'])
        elif m['cmd'] == 'cycle_scale':
            self.sequencer.cycle_scale(m['dir'])
        elif m['cmd'] == 'swap_drum_inst':
            self.sequencer.swap_drum_inst()
        elif m['cmd'] == 'change_octave':
            self.sequencer.change_octave(m['octave'])
        elif m['cmd'] == 'note':
            self.sequencer.touch_note(m['x'], m['y'])
        elif m['cmd'] == 'ins':
            self.sequencer.current_visible_instrument = m['ins']
        elif m['cmd'] == 'inc_rep':
            self.sequencer.inc_rep(m['page'])
        elif m['cmd'] == 'dec_rep':
            self.sequencer.dec_rep(m['page'])
        elif m['cmd'] == 'add_page':
            self.sequencer.add_page()
        elif m['cmd'] == 'change_division':
            self.sequencer.change_division(m['div'])
        return

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        self.beatclockcount += 1
        if self.beatclockcount >= 3:
            self.beatclockcount %= 3
            return True
        return False

    def draw(self):
        status = self.sequencer.get_status()
        led_grid = self.sequencer.get_led_grid()
        self.display.draw_all(status, led_grid)

    def save(self):
        print("Saving current grid to {}.cell".format(datetime.now()))
        filename = './saved/' + str(datetime.now()).split('.')[0] + '.json'
        with open(filename, 'w') as savefile:
            saved = self.sequencer.save()
            dump(saved, savefile)


def console_main(stdscr):
    from console import Display
    m = curses.mousemask(1)
    curses.mouseinterval(10)
    stdscr.nodelay(1)
    display = Display(stdscr)
    with mido.open_output('SuperCell_Out', autoreset=True, virtual=True) as mport:
        with mido.open_input('SuperCell_In', autoreset=True, virtual=True) as mportin:
            controller = Controller(display, mport, mportin)
            controller.run()

def hardware_main():
    from hardware import Display
    display = Display()
    with mido.open_output('SuperCell_Out', autoreset=True, virtual=True) as mport:
        with mido.open_input('SuperCell_In', autoreset=True, virtual=True) as mportin:
            controller = Controller(display, mport, mportin)
            controller.sequencer.instruments[0].add_page(0)
            controller.sequencer.instruments[0].add_page(1)
            controller.sequencer.instruments[0].inc_page_repeats(0)
            controller.sequencer.instruments[0].inc_page_repeats(0)
            controller.sequencer.instruments[0].add_page(1)
            controller.sequencer.instruments[0].inc_page_repeats(1)
            controller.sequencer.instruments[0].inc_page_repeats(0)
            controller.sequencer.instruments[3].add_page(1)
            controller.sequencer.instruments[3].add_page(1)
            controller.sequencer.instruments[3].inc_page_repeats(0)
            controller.run()

if __name__ == '__main__':
    if not args.hw:
        import curses
        curses.wrapper(console_main)
    else:
        hardware_main()
