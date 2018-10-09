from sequencer import Sequencer
from display import Display
from time import sleep, time
from datetime import datetime
import curses
from constants import *
import mido
from json import dump, load
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--set", help="Filename of previous set to load", type=str)
args = parser.parse_args()
print(args.set)

class Controller(object):
    """docstring for Controller."""
    def __init__(self, stdscr, mport, mportin):
        super(Controller, self).__init__()

        self.mport = mport
        self.mportin = mportin
        # Check for loading previous set
        if args.set:
            saved = args.set
            with open(saved, 'r') as saved_file:
                saved_set = load(saved_file)
            self.sequencer = Sequencer(mport, saved=saved_set)
        else:
            self.sequencer = Sequencer(mport, saved=None)
        self.last = time()
        self.stdscr = stdscr
        self.display = Display(stdscr)
        self.beatclockcount = 0

    def run(self):
        self.draw()
        self.stdscr.refresh()
        while True:
            if self.get_midi_tick():
                self.sequencer.step_beat()
                self.draw()
            key = self.get_keys()
            if key:
                self.draw()
                pass
            sleep(0.002)
            self.stdscr.refresh()
        pass

    def get_keys(self):
        c = self.stdscr.getch()
        if c == -1:
            return None
        if c == ord('Q'):
            self.save()
            exit()
        if c == ord(' '):
            self.sequencer.step_beat()
        if c == ord('n'):
            self.sequencer.cycle_key(-1)
        if c == ord('m'):
            self.sequencer.cycle_key(1)
        if c == ord('['):
            self.sequencer.change_division(-1)
        if c == ord(']'):
            self.sequencer.change_division(1)
        if c == ord('v'):
            self.sequencer.cycle_scale(-1)
        if c == ord('b'):
            self.sequencer.cycle_scale(1)
        if c == ord('c'):
            self.sequencer.swap_drum_inst()
        if c == ord('z'):
            self.sequencer.change_octave(-1)
        if c == ord('x'):
            self.sequencer.change_octave(1)
        if c == curses.KEY_MOUSE:
            m = curses.getmouse()
            x = self.display.get_mouse_zone(m)
            self.stdscr.addstr(23, 20, str(x))
            if x['zone'] == 'note':
                self.sequencer.touch_note(x['x'], x['y'])
            elif x['zone'] == 'ins':
                self.sequencer.current_visible_instrument = x['ins']
            elif x['zone'] == 'inc_rep':
                self.sequencer.inc_rep(x['page'])
            elif x['zone'] == 'dec_rep':
                self.sequencer.dec_rep(x['page'])
            elif x['zone'] == 'add_page':
                self.sequencer.add_page()
            elif x['zone'] == 'change_division':
                self.sequencer.change_division(x['div'])
        return str(c)

    # def get_clock_tick(self):
    #     return self.get_midi_tick()
    #     x = time()
    #     diff = x - self.last
    #     if diff > 0.3:  # 0.3 ms since last tick
    #         self.last = x
    #         return True
    #     return False

    def get_midi_tick(self):
        for message in self.mportin.iter_pending():
            if message.type == "clock":
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


def main(stdscr):
    m = curses.mousemask(1)
    curses.mouseinterval(10)
    stdscr.nodelay(1)
    with mido.open_output('SuperCell_Out', autoreset=True, virtual=True) as mport:
        with mido.open_input('SuperCell_In', autoreset=True, virtual=True) as mportin:
            controller = Controller(stdscr, mport, mportin)
            controller.run()

if __name__ == '__main__':
    curses.wrapper(main)
