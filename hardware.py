#coding=utf-8
from constants import *

import curses
from curses.textpad import rectangle
import locale
locale.setlocale(locale.LC_ALL, '')

class Display(object):
    """docstring for Display."""
    def __init__(self, serialport, w=W, h=H):
        super(Display, self).__init__()
        self.serialport = serialport
        self.grid_h = h
        self.grid_w = w
        return

    def get_button_presses(self):
        """Check serial in port for messages. If commands come in, delegate calls to relevant components"""
        return {'zone': None}
        return {'zone': 'note', 'x': grid_x, 'y': self.grid_h - grid_y -1}
        return {'zone': 'ins', 'ins': ins}
        return {'zone': 'add_page'}
        return {'zone': 'change_division', 'div': (-1 if (x-self.page_x <=5) else 1)}
        return {'zone': 'dec_rep', 'page': y-self.page_y-1}
        return {'zone': 'page_down', 'page': y-self.page_y-1}
        return {'zone': 'page_up', 'page': y-self.page_y-1}
        return {'zone': 'inc_rep', 'page': y-self.page_y-1}

    def draw_all(self, status, led_grid):
        """Send commands to serial out which describe display status:
        Typically, LED grid data, plus auxillary status of instruments, pages etc.
        Each RGB pixel's data is 24bit number.
        24bits*256pixels/1Byte = 768Bytes. Max Bitrate = 14400B/s. Refresh rate, latency = 1/18s.
        18fps is good, but is 1/18s latency acceptable?
        We know most of the display state ahead of time, is it possible to compensate for latency?
        If full LED grid is too much data, only send diffs, but do full refresh every x frames"""
        buffer = []
        for c, column in enumerate(led_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                R,G,B = LED_DISPLAY[cell]
                buffer.append(R,G,B)
        status_stream = convert_somehow(status)
        stream.append(status_stream)
        stream = ''.join(buffer)
        serial.write(stream)
        return

    def draw_gui(self, status):
        self.stdscr.addstr(1, self.grid_x+2, "S U P E R C E L L")#, curses.color_pair(4))
        status_strs = {
            'key': status.get('key'),
            'scale': status.get('scale')[:5].rjust(5),
            'octave': status.get('octave'),
            'type': "Drum" if (status.get('isdrum')==True) else "Inst",
            'division': status.get('division')
        }
        status_line_2 = "{key} {scale} +{octave}ve {type} >{division} ".format(**status_strs)
        self.stdscr.addstr(self.grid_y-1, self.grid_x+2, status_line_2)#, curses.color_pair(4))
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

    def draw_all(self, status, led_grid):
        self.draw_gui(status)
        self.draw_grid(led_grid)
        return


if __name__ == '__main__':
    display = Display()
