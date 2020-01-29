# coding=utf-8
import constants as c
import curses
import locale
from interfaces.lcd import lcd
locale.setlocale(locale.LC_ALL, '')
from time import sleep
from threading import Thread
from color_scheme import select_scheme, next_scheme  # TODO add gbl button to cycle scheme

class Display(Thread):
    """docstring for Display."""

    def __init__(self, stdscr, button_bus, led_bus, w=c.W, h=c.H):
        # super(Display, self).__init__()
        Thread.__init__(self, name='Display')
        self.button_bus = button_bus
        self.led_bus = led_bus

        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.stdscr = stdscr
        self.grid_h = h
        self.grid_w = w*2
        self.grid_x = 5
        self.grid_y = 3
        self.ins_x = self.grid_x+self.grid_w+3
        self.ins_y = self.grid_y
        self.ins_w = 4
        self.ins_h = c.MAX_INSTRUMENTS + 2
        self.page_x = self.ins_x + self.ins_w + 1
        self.page_y = self.grid_y
        self.page_w = 9
        self.page_h = c.MAX_INSTRUMENTS + 2
        self.col_scheme = select_scheme('default')
        return
    
    def run(self):
        c.debug("Display thread started")
        while True:
            sleep(0.01)
            m = self.get_cmds()
            if m.get('cmd') != None:
                c.debug(m)
                self.button_bus.put(m)
            if not self.led_bus.empty():
                status, led_grid = self.led_bus.get()
                self.draw_all(status, led_grid)

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
            return {'cmd': 'note', 'x': grid_x, 'y': self.grid_h - grid_y - 1}
        # TODO Scroll detection on encoder boxes
        # If x, y in grids1-4
        # If m[4] = click, send relevant encoder button press
        # If m[4] = scroll up/down, send relevant encoder cmds
        # 134217728 = up  A_LOW
        # 524288 = down  BUTTON4_PRESSED

        return {'cmd': None}

    def draw_stats(self, status):
        self.stdscr.addstr(1, self.grid_x+2, "C O N D U C T O R")  # , curses.color_pair(4))
        lines = ["{}: {}        ".format(k, v) for k, v in status.items()]
        for i, line in enumerate(lines):
            self.stdscr.addstr(self.grid_y+18+i, self.grid_x+2, line)  # , curses.color_pair(4))
        self.stdscr.addstr(self.grid_y+18+len(lines)+1, self.grid_x+2, lcd.flash_line)  # , curses.color_pair(4))
        return

    def draw_screens(self, text):
        for i in range(4):
            num_lines = 4
            num_chars = 16
            win = curses.newwin(num_lines+2, num_chars+2, self.grid_y+(i*6), self.grid_w+self.grid_x + 10)
            win.border()
            win.addstr(1,1,"foo")
            win.addstr(2,1,"fooobarrfizzbuzz")
            win.addstr(3,1,"foo")
            win.addstr(4,1,"foo")
            win.refresh()
        return

    def draw_grid(self, led_grid):
        '''Take a led_grid/array from the sequencer and print it to the screen'''
        sx = self.grid_x
        sy = self.grid_y
        win = curses.newwin(self.grid_h+2, self.grid_w+2, sy, sx)
        win.border()
        for i, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                x = (i * 2) + 1
                y = (c.H - r - 1) + 1
                glyph = c.DISPLAY[cell]
                # color = self.col_scheme.get_color(cell, x, y)
                # c.debug(color)
                win.addstr(y, x, glyph, curses.color_pair(40))
        win.refresh()
        return

    def draw_all(self, status, led_grid):
        self.draw_stats(status)
        self.draw_grid(led_grid)
        self.draw_screens("foo")
        return
