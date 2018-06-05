from sequencer import Sequencer
from cursor import Cursor
from time import sleep, time
import curses
from constants import *

# TODO
# Create nice GUI, overlay, buttons, info etc on screen
# sequencer shouldn't print anything, just provide grid data structure
# controller converts to symbols, adds cursor, positions grid in center, passes
# events (button presses etc_ to sequencer


class Controller(object):
    """docstring for Controller."""
    def __init__(self, stdscr):
        super(Controller, self).__init__()
        self.sequencer = Sequencer()
        self.last = time()
        self.stdscr = stdscr
        self.cursor_x = 0
        self.cursor_y = 0


    def run(self):
        while True:
            if self.get_clock_tick():
                self.sequencer.step_beat()
                self.draw()
            key = self.get_keys()
            if key:
                # Deal with key input
                # return()
                self.draw()
                # self.stdscr.addstr(str(key) + ' ')
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
            self.cursor_y = self.cursor_y - 1
        elif c == curses.KEY_UP:
            self.cursor_y = self.cursor_y + 1
        elif c == curses.KEY_RIGHT:
            self.cursor_x = self.cursor_x + 1
        elif c == curses.KEY_LEFT:
            self.cursor_x = self.cursor_x - 1
        self.cursor_x = max(0, self.cursor_x)
        self.cursor_x = min(W-1, self.cursor_x)
        self.cursor_y = max(0, self.cursor_y)
        self.cursor_y = min(H-1, self.cursor_y)
        if c == 10:
            self.sequencer.touch_note(self.cursor_x, self.cursor_y)
        if c == ord('q'):
            exit()
        return str(c)

    def get_clock_tick(self):
        x = time()
        diff = x - self.last
        # print (dir(diff))
        # print(diff)
        if diff > 0.3:  # 0.3 ms since last tick
            self.last = x
            return True
        return False

    def draw(self):
        self.sequencer.draw(self.stdscr)
        self.stdscr.addstr(H-self.cursor_y-1, self.cursor_x*2, DISPLAY[LED_CURSOR])#, curses.color_pair(4))
        self.stdscr.addstr(20, 40, "x{}, y{}".format(self.cursor_x, self.cursor_y))#, curses.color_pair(4))



def main(stdscr):
    stdscr.nodelay(1)
    controller = Controller(stdscr)
    controller.sequencer.touch_note(3,3)
    controller.sequencer.touch_note(10,4)
    controller.sequencer.touch_note(4,6)
    controller.run()


if __name__ == '__main__':
    curses.wrapper(main)
