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
        self.grid_offset_y = 3

        return

    def draw_gui(self, status):
        self.stdscr.addstr(1, self.grid_offset_x+2, "S U P E R C E L L")#, curses.color_pair(4))

        # Box around the grid
        # rectangle(self.stdscr, self.grid_offset_y - 1,
        #                        self.grid_offset_x - 1,
        #                        self.grid_offset_y+self.grid_height,
        #                        self.grid_offset_x+(2 * self.grid_width)+1)
        # status_strs = {
        #     'ins_num': status.get('ins_num').rjust(2),
        #     'ins_tot': status.get('ins_total').ljust(2),
        #     'page_num': status.get('page_num').rjust(2),
        #     'page_tot': status.get('page_total').ljust(2),
        #     'repeat_num': status.get('repeat_num').rjust(2),
        #     'repeat_tot': status.get('repeat_total').ljust(2),
        #     'key': status.get('key'),
        #     'scale': status.get('scale')[:5].rjust(5),
        #     'octave': status.get('octave'),
        # }
        # status_line_1 = "Page: {page_num}/{page_tot} Repeat: {repeat_num}/{repeat_tot}  ".format(**status_strs)
        # status_line_2 = "Scale: {key} {scale} +{octave}ve".format(**status_strs)
        button_line = "Switch Instrument:  < >   New Page: :;  +/- Repeats: {[ ]}"
        # self.stdscr.addstr(self.grid_height+self.grid_offset_y+5, self.grid_offset_x, status_line_1)#, curses.color_pair(4))
        # self.stdscr.addstr(self.grid_height+self.grid_offset_y+6, self.grid_offset_x, status_line_2)#, curses.color_pair(4))
        self.stdscr.addstr(self.grid_height+self.grid_offset_y+7, self.grid_offset_x, button_line)#, curses.color_pair(4))
        self.stdscr.addstr(self.grid_height+self.grid_offset_y+6, self.grid_offset_x, str(status['page_stats']))#, curses.color_pair(4))
        self.draw_ins_selector(status['ins_num'], status['ins_total'])
        self.draw_pages(status['page_num'], status['repeat_num'], status['page_stats'])
        return

    def draw_ins_selector(self, ins_num, ins_tot):
        sx = self.grid_offset_x+(self.grid_width*2)+3
        sy = self.grid_offset_y
        win = curses.newwin(ins_tot+2, 4, sy, sx)
        win.border()
        # Inactive instruments
        for i in range(self.grid_height):
            win.addstr(i+1, 1, DISPLAY[1])
        # Active instrument
        win.addstr(ins_num, 1, DISPLAY[3])
        win.refresh()
        return

    def draw_pages(self, page_num, repeat_num, page_repeats):
        page_tot = len(page_repeats)
        win = curses.newwin(page_tot+2, 4, self.grid_offset_y, self.grid_offset_x+self.grid_width*2+8)
        for i in range(page_tot):
            win.addstr(i+1, 2, str(page_repeats[i]))# DISPLAY[3])
        win.border()
        win.refresh()

    def draw_grid(self, led_grid, cursor_pos):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_offset_x
        sy = self.grid_offset_y
        win = curses.newwin(self.grid_height+2, (self.grid_width*2)+2, sy, sx)
        win.border()
        for c, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                x = (c*2) + 1
                y = (H-r-1) + 1
                glyph = DISPLAY[cell]
                win.addstr(y, x, glyph)#, curses.color_pair(4))
        self.draw_cursor(win, cursor_pos)
        win.refresh()
        return

    def draw_cursor(self, win, cursor):
        '''Draw the cursor over the grid'''
        x = (cursor['x']*2) + 1
        y = (self.grid_height-cursor['y']-1) + 1
        glyph = DISPLAY[LED_CURSOR]
        win.addstr(y, x, glyph)#, curses.color_pair(4))
        return

    def draw_all(self, status, led_grid, cursor_pos):
        self.draw_gui(status)
        self.draw_grid(led_grid, cursor_pos)
        return


if __name__ == '__main__':
    display = Display()
