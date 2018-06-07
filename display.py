#coding=utf-8
from constants import *

import curses
import locale
locale.setlocale(locale.LC_ALL, '')


class Display(object):
    """docstring for Display."""
    def __init__(self, stdscr, w=W, h=H):
        super(Display, self).__init__()
        self.stdscr = stdscr


        self.stdscr = stdscr
        self.grid_height = h
        self.grid_width = w

        # self.cursor = Cursor()
        # self.sequencer = Sequencer()
        return

    def draw_cursor(self, cursor):
        '''Draw the cursor over the grid'''
        self.stdscr.addstr(self.grid_height-cursor.y-1, cursor.x*2, DISPLAY[LED_CURSOR])#, curses.color_pair(4))
        return

    def draw_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        return

    def draw_all(self):
        return

    def draw_gui(self):
        return


if __name__ == '__main__':
    display = Display()
