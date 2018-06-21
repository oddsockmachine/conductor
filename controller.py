from sequencer import Sequencer
from display import Display
from time import sleep, time
import curses
from constants import *
import mido


class Controller(object):
    """docstring for Controller."""
    def __init__(self, stdscr, mport, mportin):
        super(Controller, self).__init__()
        self.mport = mport
        self.mportin = mportin
        self.sequencer = Sequencer(mport, key="e", scale="pentatonic_maj")
        self.last = time()
        self.stdscr = stdscr
        self.display = Display(stdscr)
        self.beatclockcount = 0

    def run(self):
        while True:
            if self.get_midi_tick():
                self.sequencer.step_beat()
                self.draw()
            key = self.get_keys()
            if key:
                # Deal with key input
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
            exit()
        if c == ord('.'):  # > without shift
            self.sequencer.next_instrument()
        if c == ord(','):  # < without shift
            self.sequencer.prev_instrument()
        if c == ord(";"):  # Add page immediately after current
            self.sequencer.get_curr_instrument().add_page(True)
        if c == ord("'"):  # Add page to end of list
            self.sequencer.get_curr_instrument().add_page(False)
        if c == ord('['):
            self.sequencer.get_curr_instrument().get_curr_page().dec_repeats()
        if c == ord(']'):
            self.sequencer.get_curr_instrument().get_curr_page().inc_repeats()
        if c == ord(' '):
            self.sequencer.step_beat()
        if c == ord('n'):
            self.sequencer.cycle_key(-1)
        if c == ord('m'):
            self.sequencer.cycle_key(1)
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
            self.stdscr.addstr(50, 50, str(x))
            if x['zone'] == 'note':
                self.sequencer.touch_note(x['x'], x['y'])
            elif x['zone'] == 'ins':
                self.sequencer.current_visible_instrument = x['ins']

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
        if self.beatclockcount >= 12:
            self.beatclockcount %= 12
            return True
        return False

    def draw(self):
        status = self.sequencer.get_status()  # TODO from sequencer?
        led_grid = self.sequencer.get_led_grid()
        self.display.draw_all(status, led_grid)



def main(stdscr):
    curses.mousemask(1)
    stdscr.nodelay(1)
    with mido.open_output('Flynn', autoreset=True, virtual=True) as mport:
        with mido.open_input('Flynn_In', autoreset=True, virtual=True) as mportin:
            controller = Controller(stdscr, mport, mportin)
            controller.run()

if __name__ == '__main__':
    curses.wrapper(main)
