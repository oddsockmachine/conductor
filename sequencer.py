#coding=utf-8
from time import sleep
from constants import *
from instrument import Instrument
# from multiprocessing.connection import Listener

class Sequencer(object):
    """docstring for Sequencer."""
    def __init__(self, mport, bars=int(W/4)):
        super(Sequencer, self).__init__()
        self.mport = mport
        self.instruments = [Instrument(0, self.mport, "e", "major", octave=2, bars=bars)]  # limit to 16 midi channels
        self.current_visible_instrument = 0
        self.max_num_instruments = MAX_INSTRUMENTS
        # self.tempo = 20
        self.beat_position = 0
        self.height = H
        self.width = bars*4
        self.mport = mport

    # def inc_tempo(self, amt):
    #     self.tempo += amt
    #     return
    #
    # def dec_tempo(self, amt):
    #     self.tempo -= amt
    #     return

    def add_instrument(self, key, scale, octave=2, bars=int(W/4), height=H):
        if len(self.instruments) == 16:
            logging.warning('Already at 16 instruments')
            return False
        ins_num = len(self.instruments)
        self.instruments.append(Instrument(ins_num, self.mport, key, scale, octave, bars, height))
        return

    def next_instrument(self):
        if self.current_visible_instrument == len(self.instruments)-1:
            logging.warning('Reached end of instruments')
            return False
        self.current_visible_instrument += 1
        return

    def prev_instrument(self):
        if self.current_visible_instrument == 0:
            logging.warning('Reached start of instruments')
            return False
        self.current_visible_instrument -= 1
        return

    def step_beat(self):
        self.beat_position += 1
        self.beat_position %= self.width
        for ins in self.instruments:
            ins.step_beat()#self.beat_position)
        pass

    def get_curr_instrument(self):
        return self.instruments[self.current_visible_instrument]

    def touch_note(self, x, y):
        self.get_curr_instrument().touch_note(x, y)

    def get_led_grid(self):
        note_grid = self.get_curr_instrument().get_curr_page_grid()
        led_grid = []
        for c in range(self.width):
            col = []
            for r in range(self.height):
                col.append()
        for c, column in enumerate(note_grid):  # row counter
            led_col = []
            for r, cell in enumerate(column):  # column counter
                if cell == NOTE_ON:
                    scr.addstr(H-r-1, c*2, DISPLAY[NOTE_ON])#, curses.color_pair(4))
                elif c == self.beat_position: # and DISPLAY[y] != LED_ACTIVE:
                    scr.addstr(H-r-1, c*2, DISPLAY[LED_SELECT])#, curses.color_pair(4))
                else:
                    scr.addstr(H-r-1, c*2, DISPLAY[LED_BLANK])#, curses.color_pair(4))
        return


    def draw(self, scr):
        note_grid = self.get_curr_instrument().get_curr_page_grid()
        for c, column in enumerate(note_grid):  # row counter
            for r, cell in enumerate(column):  # column counter
                if cell == NOTE_ON:
                    scr.addstr(H-r-1, c*2, DISPLAY[NOTE_ON])#, curses.color_pair(4))
                elif c == self.beat_position: # and DISPLAY[y] != LED_ACTIVE:
                    scr.addstr(H-r-1, c*2, DISPLAY[LED_SELECT])#, curses.color_pair(4))
                else:
                    scr.addstr(H-r-1, c*2, DISPLAY[LED_BLANK])#, curses.color_pair(4))
        return




if __name__ == '__main__':
    seq = Sequencer(None)
    seq.touch_note(1,3)
    # seq.run()
    # try:
    #     print("foo")
    #     # sequencer.run()
    # except KeyboardInterrupt:
    #     print 'Interrupted'
    #     # try:
    #     sequencer.listener.close()
    #     sys.exit(0)
    #     # except SystemExit:
    #     #     os._exit(0)


    seq.next_instrument()
    seq.prev_instrument()
    seq.prev_instrument()
    seq.touch_note(3,3)
    for i in range(20):
        seq.step_beat()
        seq.get_curr_instrument().print_curr_page_notes()
