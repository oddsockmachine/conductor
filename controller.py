from sequencer import Sequencer
from time import sleep, time
import curses

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



    def run(self):
        while True:
            if self.get_clock_tick():
                self.sequencer.step_beat()
                self.sequencer.output(self.stdscr)
            key = self.get_keys()
            if key:
                # Deal with key input
                # if key == ord('q'):
                exit()
                # self.sequencer.output(self.stdscr)
                # self.stdscr.addstr(str(key) + ' ')
                pass
            sleep(0.05)
            self.stdscr.refresh()
        pass

    def get_keys(self):
        c = self.stdscr.getch()
        if c != -1:
            return str(c)
        return None

    def get_clock_tick(self):
        x = time()
        diff = x - self.last
        # print (dir(diff))
        # print(diff)
        if diff > 0.3:
            self.last = x
            return True
        return False


def main(stdscr):
    stdscr.nodelay(1)
    controller = Controller(stdscr)
    controller.run()

if __name__ == '__main__':
    curses.wrapper(main)
