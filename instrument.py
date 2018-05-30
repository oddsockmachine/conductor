#coding=utf-8
# from time import sleep
from constants import *
from note_grid import Note_Grid

class Instrument(object):
    """docstring for Instrument."""
    def __init__(self, name, key, scale, octave, bars=W/4, height=H):
        super(Instrument, self).__init__()
        self.name = name
        self.height = height
        self.bars = min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.beat_position = 0
        self.pages = [Note_Grid(self.bars, self.height)]
        self.key = "a"
        self.scale = "pentatonic"
        self.octave = 2  # Starting octave

    def get_curr_page(self):
        return self.pages[self.curr_page_num]


    def add_page(self, pos=-1):
        '''Add or insert a new blank page into the list of pages'''
        self.pages.insert(pos, Note_Grid(self.bars, self.height))
        return

    def set_next_page(self):
        '''Override and skip to a particular page when the beat reaches the end'''
        return
    def cell_to_midi(self, cell):
        '''convert a cell height to a midi note based on key, scale, octave'''
        return

    def touch_note(self, x, y):
        '''touch the x/y cell on the current page'''
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.touch_note(x, y)
        return True

    def add_note(self, x, y, page=False):
        '''force-on a x/y cell on the current page'''
        # if not page:
        #     page = self.get_curr_page()
        # if page > len(self.pages):
        #     logging.warning('Requested page {} > {}'.format(page, len(self.pages)))
        #     return False
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.add_note(x, y)
        return

    def del_note(self, x, y):
        page = self.get_curr_page()
        if not page.validate_touch(x, y):
            return False
        page.del_note(x, y)
        return

    def get_notes_from_curr_beat(self):
        return

    def get_curr_page_grid(self):
        # page = self.get_curr_page()
        return self.get_curr_page().note_grid

    def print_curr_page_notes(self):
        grid = self.get_curr_page_grid()
        display = {0: '. ', 1: '░░', 2:'▒▒', 3:'▓▓'}
        for r, row in enumerate(grid):  # row counter
            for c, cell in enumerate(row):  # column counter
                if c == self.beat_position: # and display[y] != LED_ACTIVE:
                    print(display[LED_SELECT]),
                else:
                    print(display[cell]),
            print('')
        print('')

    def inc_curr_page_repeats(self):
        '''Increase how many times the current page will loop'''
        self.get_curr_page().inc_repeats()
        return

    def dec_curr_page_repeats(self):
        '''Reduce how many times the current page will loop'''
        self.get_curr_page().dec_repeats()
        return

    def step_beat(self, beat=None):
        '''Increment the beat counter, and do the math on pages and repeats'''
        if beat:
            self.beat_position = beat
            return
        self.beat_position += 1
        if self.beat_position == self.width:
            self.beat_position = 0
            # print("page done")
            self.curr_rept_num += 1
            if self.curr_rept_num == self.get_curr_page().repeats:
                self.curr_rept_num = 0
                self.curr_page_num += 1
                # print("next page")
                self.curr_page_num %= len(self.pages)
        # print("b{}/{}, p{}/{}, r{}/{}".format(self.beat_position, self.width, self.curr_page_num+1, len(self.pages), self.curr_rept_num+1, self.get_curr_page().repeats))
        return

if __name__ == '__main__':
    ins = Instrument("foo", "a", "pentatonic", 2)
    ins.touch_note(4,4)
    ins.touch_note(5,5)
    ins.touch_note(6,6)
    ins.touch_note(6,6)
    ins.add_note(1,1)
    ins.add_note(0,0)
    ins.inc_curr_page_repeats()

    ins.inc_curr_page_repeats()

    ins.print_curr_page_notes()
    ins.add_page(1)
    ins.add_page(2)
    for i in range(20):
        ins.step_beat()
        ins.print_curr_page_notes()
        # sleep(0.1)
    # ins.inc_curr_page_repeats()

    for i in range(40):
        ins.step_beat()
        ins.print_curr_page_notes()
        # sleep(0.1)

    # ins.curr_page_num = 1
    # ins.touch_note(15,15)
    # ins.print_curr_page_notes()
    # ins.curr_page_num = 2
    # ins.print_curr_page_notes()
