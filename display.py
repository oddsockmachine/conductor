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
        self.grid_width = w*2
        self.grid_offset_x = 5
        self.grid_offset_y = 3
        self.ins_x = self.grid_offset_x+self.grid_width+3
        self.ins_y = self.grid_offset_y
        self.ins_w = 4
        self.ins_h = 18

        return

    def get_mouse_zone(self, m):
        '''Return which zone the mouse clicked on'''
        x = m[1]
        y = m[2]
        # convert x/y to led_grid coords
        if x > self.grid_offset_x and x <= self.grid_offset_x+self.grid_width and y > self.grid_offset_y and y <= self.grid_offset_y+self.grid_height:
            grid_x = int((x-6)/2)
            grid_y = int(y-4)
            return {'zone': 'note', 'x': grid_x, 'y': self.grid_height - grid_y -1}
        if x > self.ins_x and x < self.ins_x+self.ins_w and y < self.ins_y+self.ins_h and y > self.ins_y:
            ins = y - self.ins_y - 1
            return {'zone': 'ins', 'ins': ins}
        return {'zone': None}

    def draw_gui(self, status):
        self.stdscr.addstr(1, self.grid_offset_x+2, "S U P E R C E L L")#, curses.color_pair(4))
        status_strs = {
            'key': status.get('key'),
            'scale': status.get('scale')[:5].rjust(5),
            'octave': status.get('octave'),
            'type': "Drum" if (status.get('isdrum')==True) else "Inst"
        }
        status_line_2 = "{key} {scale} +{octave}ve {type} ".format(**status_strs)
        button_line = "Switch Instrument:  < >   New Page: :;  +/- Repeats: {[ ]}"
        self.stdscr.addstr(self.grid_offset_y-1, self.grid_offset_x+2, status_line_2)#, curses.color_pair(4))
        self.stdscr.addstr(self.grid_height+self.grid_offset_y+2, self.grid_offset_x, button_line)#, curses.color_pair(4))
        self.draw_ins_selector(status['ins_num'], status['ins_total'])
        self.draw_pages(status['page_num'], status['repeat_num'], status['page_stats'])
        return

    def draw_ins_selector(self, ins_num, ins_tot):
        # sx = self.ins_x
        # sy = self.ins_y
        win = curses.newwin(self.ins_h, self.ins_w, self.ins_y, self.ins_x)
        win.border()
        # Inactive instruments
        for i in range(self.grid_height):
            win.addstr(i+1, 1, DISPLAY[1])
        # Active instrument
        win.addstr(ins_num, 1, DISPLAY[3])
        win.refresh()
        return

    def draw_pages(self, curr_page, repeat_num, page_repeats):
        page_tot = len(page_repeats)
        win = curses.newwin(18, 7, self.grid_offset_y, self.grid_offset_x+self.grid_width+8)
        for i in range(16):
            win.addstr(i+1, 1, str("    "))# DISPLAY[3])
        for i in range(page_tot):
            win.addstr(i+1, 3, str(str(page_repeats[i]) + "+-"))# DISPLAY[3])
        win.addstr(page_tot+1, 3, "+")# DISPLAY[3])
        win.addstr(curr_page, 1, str(repeat_num)+"/")# DISPLAY[3])
        win.border()
        win.refresh()

    def draw_grid(self, led_grid, cursor_pos):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_offset_x
        sy = self.grid_offset_y
        win = curses.newwin(self.grid_height+2, (self.grid_width)+2, sy, sx)
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
