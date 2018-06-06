#coding=utf-8
# from time import sleep
from constants import *
from note_grid import Note_Grid
from note_conversion import create_cell_to_midi_note_lookup, scales, keys
import mido

class Instrument(object):
    """docstring for Instrument."""
    def __init__(self, ins_num, mport, key, scale, octave=2, bars=W/4, height=H):
        super(Instrument, self).__init__()
        if not isinstance(ins_num, int):
            print("Instrument num {} must be an int".format(ins_num))
            exit()
        self.ins_num = ins_num  # Number of instrument in the sequencer - corresponds to midi channel
        self.mport = mport
        logging.info(mport)

        self.height = height
        self.bars = bars #min(bars, W/4)  # Option to reduce number of bars < 4
        self.width = self.bars * 4
        self.curr_page_num = 0
        self.curr_rept_num = 0
        self.beat_position = 0
        self.pages = [Note_Grid(self.bars, self.height)]
        if key not in keys:
            print('Requested key {} not known'.format(key))
            exit()
        self.key = key
        if scale not in scales.keys():
            print('Requested scale {} not known'.format(scale))
            exit()
        self.scale = scale
        self.octave = octave  # Starting octave
        self.old_notes = []  # Keep track of currently playing notes so we can off them next step
        self.note_converter = create_cell_to_midi_note_lookup(scale, octave, key, height)

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
        midi_note_num = self.note_converter[cell]
        return midi_note_num

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
                    print(display[LED_SELECT], end='')
                else:
                    print(display[cell], end='')
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
        # if beat:
        #     self.beat_position = beat
        #     return
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
        new_notes = self.get_curr_notes()
        self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def get_curr_notes(self):
        grid = self.get_curr_page_grid()
        beat_pos = self.beat_position
        beat_notes = [row[beat_pos] for row in grid][::-1]  # extract column from grid
        notes_on = [i for i, x in enumerate(beat_notes) if x == NOTE_ON]  # get list of cells that are on
        return notes_on


    def output(self, old_notes, new_notes):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        logging.info(self.beat_position)

        notes_off = [self.cell_to_midi(c) for c in old_notes]
        notes_on = [self.cell_to_midi(c) for c in new_notes]
        logging.info(notes_on)
        logging.info(notes_off)
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        logging.info(on_msgs)
        logging.info(off_msgs)
        msgs = off_msgs + on_msgs
        # logging.info(msgs)
        for msg in msgs:
            logging.info(msg)
            self.mport.send(msg)




if __name__ == '__main__':
    from time import sleep
    with mido.open_output('Flynn', autoreset=True, virtual=True) as mport:

        print(mport)
        sleep(1)
        on = mido.Message('note_on', note=61)
        print('Sending {}'.format(on))
        mport.send(on)

        ins = Instrument(8, mport, "a", "pentatonic", octave=2, bars=4)
        ins.touch_note(4,4)
        ins.touch_note(5,5)
        ins.touch_note(6,6)
        ins.touch_note(6,7)
        ins.touch_note(6,5)
        ins.touch_note(7,6)
        ins.add_note(1,1)
        ins.add_note(0,0)
        # ins.inc_curr_page_repeats()
        #
        # ins.inc_curr_page_repeats()
        #
        # ins.print_curr_page_notes()
        # ins.add_page(1)
        # ins.add_page(2)
        for i in range(50):
            ins.step_beat()
            sleep(0.2)
            ins.print_curr_page_notes()
            # sleep(0.1)
        # ins.inc_curr_page_repeats()

        # for i in range(40):
        #     ins.step_beat()
        #     ins.print_curr_page_notes()
        #     # sleep(0.1)

        # ins.curr_page_num = 1
        # ins.touch_note(15,15)
        # ins.print_curr_page_notes()
        # ins.curr_page_num = 2
        # ins.print_curr_page_notes()
