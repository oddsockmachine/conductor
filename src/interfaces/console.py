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
        if c == curses.KEY_UP:
            m['cmd'] = "LOAD"
        if c == curses.KEY_DOWN:
            m['cmd'] = "SAVE"
        if c == ord('Q'):
            m['cmd'] = 'quit'
        if c == ord('s'):
            m['cmd'] = 'toggle_save'
        if c == ord('S'):
            m['cmd'] = 'save'
        if c == ord(' '):
            m['cmd'] = 'step_beat'
        if c == ord('`'):
            m['cmd'] = 'clear_page'
        if c == ord('n'):
            m['cmd'] = 'cycle_key'
            m['dir'] = -1
        if c == ord('m'):
            m['cmd'] = 'cycle_key'
            m['dir'] = 1
        if c == ord('['):
            m['cmd'] = 'change_division'
            m['div'] = "-"
        if c == ord(']'):
            m['cmd'] = 'change_division'
            m['div'] = "+"
        if c == ord('v'):
            m['cmd'] = 'cycle_scale'
            m['dir'] = -1
        if c == ord('b'):
            m['cmd'] = 'cycle_scale'
            m['dir'] = 1
        if c == ord('c'):
            m['cmd'] = 'swap_drum_inst'
        if c == ord('z'):
            m['cmd'] = 'change_octave'
            m['dir'] = -1
        if c == ord('x'):
            m['cmd'] = 'change_octave'
            m['dir'] = 1
        if c == ord('r'):
            m['cmd'] = 'random_rpt'
        if c == ord('t'):
            m['cmd'] = 'sustain'
        # if c == ord('o'):
        #     m['cmd'] = 'chaos'
        #     m['dir'] = +1
        # if c == ord('p'):
        #     m['cmd'] = 'chaos'
        #     m['dir'] = -1
        if c == ord('/'):
            m['cmd'] = 'z_mode'
        if c in [ord('1'), ord('2'), ord('3')]:
            m['cmd'] = 'add_instrument'
            m['type'] = int(chr(c))
        if c == curses.KEY_MOUSE:
            _m = curses.getmouse()
            m = self.get_mouse_zone(_m)
        self.stdscr.addstr(23, 20, str(m))
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
        # Check for Instrument selector
        if x > self.ins_x and x < self.ins_x+self.ins_w and y < self.ins_y+self.ins_h and y > self.ins_y:
            ins = y - self.ins_y - 1
            return {'cmd': 'ins', 'ins': ins}
        # Check for Page controller
        if x > self.page_x and x < self.page_x+self.page_w and y < self.page_y+self.page_h and y > self.page_y:
            if y-self.page_y == 15:
                return {'cmd': 'add_page'}
            if y-self.page_y == 16:
                return {'cmd': 'change_division', 'div': (-1 if (x-self.page_x <=5) else 1)}
            if x-self.page_x <= 2:
                return {'cmd': 'dec_rep', 'page': y-self.page_y-1}
            if x-self.page_x >= 10:
                return {'cmd': 'page_down', 'page': y-self.page_y-1}
            if x-self.page_x >= 8:
                return {'cmd': 'page_up', 'page': y-self.page_y-1}
            if x-self.page_x >= 6:
                return {'cmd': 'inc_rep', 'page': y-self.page_y-1}
        # Check for key, scale, octave, drum buttons (still to be drawn)
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
        # self.stdscr.addstr(self.grid_y-1, self.grid_x+2, status_line_2)#, curses.color_pair(4))
        for i, line in enumerate(lines):
            self.stdscr.addstr(self.grid_y+18+i, self.grid_x+2, line)#, curses.color_pair(4))
        self.draw_ins_selector(status['ins_num'], status['ins_total'])
        self.draw_pages(status['page_num'], status['repeat_num'], status['page_stats'])
        return

    def draw_ins_selector(self, ins_num, ins_tot):
        win = curses.newwin(self.ins_h, self.ins_w, self.ins_y, self.ins_x)
        win.border()
        # Inactive instruments
        for i in range(MAX_INSTRUMENTS):
            win.addstr(i+1, 1, DISPLAY[1])
        # Active instrument
        win.addstr(ins_num, 1, DISPLAY[3])
        win.refresh()
        return

    def draw_pages(self, curr_page, repeat_num, page_repeats):
        page_tot = len(page_repeats)
        win = curses.newwin(self.page_h, self.page_w+4, self.page_y, self.page_x)
        for i in range(16):
            win.addstr(i+1, 1, str("    "))# DISPLAY[3])
        win.addstr(15, 3, "+++")  # Add page button, which will be overwritten when at 15 pages
        win.addstr(16, 3, "<<  >>")  # Add page button, which will be overwritten when at 15 pages
        for i in range(page_tot):
            win.addstr(i+1, 1, str("-   " + str(page_repeats[i]) + " + ∧ ∨"))# DISPLAY[3])
        win.addstr(curr_page, 3, str(repeat_num)+"/")# DISPLAY[3])
        win.border()
        win.refresh()

    def draw_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_x
        sy = self.grid_y
        win = curses.newwin(self.grid_h+2, (self.grid_w)+2, sy, sx)
        win.border()
        for c, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                x = (c*2) + 1
                y = (H-r-1) + 1
                glyph = DISPLAY[cell]
                win.addstr(y, x, glyph)#, curses.color_pair(4))
        win.refresh()
        return

    def draw_z_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_x
        sy = self.grid_y
        win = curses.newwin(self.grid_h+2, (self.grid_w)+2, sy, sx)
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
