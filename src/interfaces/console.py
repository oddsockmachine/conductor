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
        self.grid_h = h
        self.grid_w = w*2
        self.grid_x = 5
        self.grid_y = 3
        self.ins_x = self.grid_x+self.grid_w+3
        self.ins_y = self.grid_y
        self.ins_w = 4
        self.ins_h = MAX_INSTRUMENTS+2
        self.page_x = self.ins_x + self.ins_w + 1
        self.page_y = self.grid_y
        self.page_w = 9
        self.page_h = MAX_INSTRUMENTS+2
        return

    def get_cmds(self):
        m = {'cmd': None}
        c = self.stdscr.getch()
        if c == -1:
            m['cmd'] = None
        if c == curses.KEY_LEFT:
            m['cmd'] = "CONFIG_A"
        if c == curses.KEY_RIGHT:
            m['cmd'] = "CONFIG_B"
        # if c == curses.KEY_UP:
        #     m['cmd'] = "LOAD"
        # if c == curses.KEY_DOWN:
        #     m['cmd'] = "SAVE"
        if c == ord('Q'):
            m['cmd'] = 'quit'
        if c == ord('s'):
            m['cmd'] = 'toggle_save'
        # if c == ord('S'):
        #     m['cmd'] = 'save'
        if c == ord(' '):
            m['cmd'] = 'step_beat'
        if c == curses.KEY_MOUSE:
            _m = curses.getmouse()
            m = self.get_mouse_zone(_m)
        return m


    def get_mouse_zone(self, m):
        '''Return which zone the mouse clicked on'''
        x = m[1]
        y = m[2]
        # Check for LED Grid
        if x > self.grid_x and x <= self.grid_x+self.grid_w and y > self.grid_y and y <= self.grid_y+self.grid_h:
            grid_x = int((x-6)/2)
            grid_y = int(y-4)
            return {'cmd': 'note', 'x': grid_x, 'y': self.grid_h - grid_y -1}
        return {'cmd': None}

    def draw_gui(self, status):
        self.stdscr.addstr(1, self.grid_x+2, "S U P E R C E L L")#, curses.color_pair(4))
        status_strs = {
            'key': status.get('key'),
            'scale': status.get('scale')[:5].rjust(5),
            'octave': status.get('octave'),
            'type': status.get('type'),
            'division': status.get('division'),
            'rpt': "R" if status.get('random_rpt') else " ",
            'sustain': "S" if status.get('sustain') else " ",
        }
        status_line_2 = "{key} {scale} +{octave}ve {type} >{division}  {rpt} {sustain}".format(**status_strs)

        lines = ["{}: {}".format(k,v) for k, v in status.items()]
        for i, line in enumerate(lines):
            self.stdscr.addstr(self.grid_y+18+i, self.grid_x+2, line)#, curses.color_pair(4))
        return

    def draw_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_x
        sy = self.grid_y
        win = curses.newwin(self.grid_h+2, self.grid_w+2, sy, sx)
        win.border()
        for c, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                x = (c*2) + 1
                y = (H-r-1) + 1
                glyph = DISPLAY[cell]
                win.addstr(y, x, glyph)#, curses.color_pair(4))
        win.refresh()
        return

    def draw_all(self, status, led_grid):
        self.draw_gui(status)
        self.draw_grid(led_grid)
        return
