#coding=utf-8
from constants import *
from cursor import Cursor
from sequencer import Sequencer

import curses
import locale
locale.setlocale(locale.LC_ALL, '')


class Selector(object):
    def __init__(self):
        self.rows_selected = []
        self.columns_selected = []


class Display(object):
    def __init__(self, scr):
        self.scr = scr
        self.height = H
        self.width = W
        # self.display_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]
        # self.current_page = 0
        # self.cursor = cursor
        # self.select = select
        # self.notes = notes
        self.k = 1
        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor = Cursor()
        self.sequencer = Sequencer()
        return

    def run(self):
        print("ok")
        while self.scr.getch() != ord('q'):
            self.sequencer.output(self.scr)
            # Run seq in thread
            # seq.print
            # Add display overlay
            # handle inputs

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    display = Display(stdscr)
    display.run()


if __name__ == "__main__":
    curses.wrapper(main)
