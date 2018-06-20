from sequencer import Sequencer
from cursor import Cursor
from display import Display
from time import sleep, time
import curses
from constants import *
import mido
mido.get_output_names()
# TODO
# Create nice GUI, overlay, buttons, info etc on screen
# sequencer shouldn't print anything, just provide grid data structure
# controller converts to symbols, adds cursor, positions grid in center, passes
# events (button presses etc_ to sequencer


class Controller(object):
    """docstring for Controller."""
    def __init__(self, stdscr, mport, mportin):
        super(Controller, self).__init__()
        self.mport = mport
        self.mportin = mportin
        self.sequencer = Sequencer(mport, key="e", scale="pentatonic_maj")
        self.last = time()
        self.stdscr = stdscr
        self.cursor = Cursor()
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
            # self.draw()  # ??
        pass

    def get_keys(self):
        c = self.stdscr.getch()
        if c == -1:
            return None
        if c == curses.KEY_DOWN:
            self.cursor.move(0, -1)
        elif c == curses.KEY_UP:
            self.cursor.move(0, 1)
        elif c == curses.KEY_RIGHT:
            self.cursor.move(1, 0)
        elif c == curses.KEY_LEFT:
            self.cursor.move(-1, 0)
        if c == 10:
            self.sequencer.touch_note(self.cursor.x, self.cursor.y)
        if c == ord('q'):
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
        cursor_pos = self.cursor.get_pos()
        self.display.draw_all(status, led_grid, cursor_pos)


        # self.stdscr.addstr(20, 40, "x{}, y{}  ".format(self.cursor.x, self.cursor.y))
        # self.stdscr.addstr(19, 40, str(self.beatclockcount)+"  ")
        # self.stdscr.addstr(19, 40, str(self.sequencer.current_visible_instrument)+"  ")



def main(stdscr):
    stdscr.nodelay(1)
    with mido.open_output('Flynn', autoreset=True, virtual=True) as mport:
        with mido.open_input('Flynn_In', autoreset=True, virtual=True) as mportin:
            controller = Controller(stdscr, mport, mportin)
            controller.sequencer.touch_note(3,4)
            # controller.sequencer.get_curr_instrument().add_page(1)
            # controller.sequencer.add_instrument("a", "major", octave=2)
            # controller.sequencer.add_instrument("c", "pentatonic", octave=4, bars=4)
            # controller.sequencer.add_instrument("d", "pentatonic", octave=5, bars=4)
            controller.run()

if __name__ == '__main__':
    curses.wrapper(main)
