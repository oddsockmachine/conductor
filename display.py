#coding=utf-8
from constants import *

import curses
from curses.textpad import rectangle
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
        self.grid_offset_x = 5
        self.grid_offset_y = 1

        return

    def draw_gui(self, status):
        # Box around the grid
        rectangle(self.stdscr, self.grid_offset_y - 1,
                               self.grid_offset_x - 1,
                               self.grid_offset_y+self.grid_height,
                               self.grid_offset_x+(2 * self.grid_width)+1)
        status_strs = {
            'ins_num': status.get('ins_num').rjust(2),
            'ins_tot': status.get('ins_total').ljust(2),
            'page_num': status.get('page_num').rjust(2),
            'page_tot': status.get('page_total').ljust(2),
            'repeat_num': status.get('repeat_num').rjust(2),
            'repeat_tot': status.get('repeat_total').ljust(2),
            'key': status.get('key'),
            'scale': status.get('scale')[:5].rjust(5),
            'octave': status.get('octave'),
        }
        status_line_1 = "Instrument: {ins_num}/{ins_tot} Page: {page_num}/{page_tot} Repeat: {repeat_num}/{repeat_tot}  ".format(**status_strs)
        status_line_2 = "Scale: {key} {scale} +{octave}ve".format(**status_strs)
        button_line = "Add Instrument: /?  Switch Instrument:  < >   New Page: :;  +/- Repeats: {[ ]}"
        self.stdscr.addstr(self.grid_height+2, self.grid_offset_x-1, status_line_1)#, curses.color_pair(4))
        self.stdscr.addstr(self.grid_height+3, self.grid_offset_x-1, status_line_2)#, curses.color_pair(4))
        self.stdscr.addstr(self.grid_height+4, self.grid_offset_x-1, button_line)#, curses.color_pair(4))

        return

    def draw_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        for c, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                x = (c*2) + self.grid_offset_x
                y = (H-r-1) + self.grid_offset_y
                glyph = DISPLAY[cell]
                self.stdscr.addstr(y, x, glyph)#, curses.color_pair(4))
        return

    def draw_cursor(self, cursor):
        '''Draw the cursor over the grid'''
        x = (cursor['x']*2) + self.grid_offset_x
        y = (self.grid_height-cursor['y']-1) + self.grid_offset_y
        glyph = DISPLAY[LED_CURSOR]
        self.stdscr.addstr(y, x, glyph)#, curses.color_pair(4))
        return

    def draw_all(self, status, led_grid, cursor_pos):
        self.draw_gui(status)
        self.draw_grid(led_grid)
        self.draw_cursor(cursor_pos)
        return


if __name__ == '__main__':
    display = Display()
