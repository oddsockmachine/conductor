#coding=utf-8
from time import sleep
from constants import *
from instrument import Instrument
from note_conversion import *

class Sequencer(object):
    """docstring for Sequencer."""
    # def __init__(self, mport, bars=int(W/4)):
    def __init__(self, mport, saved=None, key="e", scale="pentatonic_maj", octave=2, bars=int(W/4), height=H):
        super(Sequencer, self).__init__()
        self.mport = mport
        if key not in KEYS:
            print('Requested key {} not known'.format(key))
            exit()
        self.key = key
        if scale not in SCALES.keys():
            print('Requested scale {} not known'.format(scale))
            exit()
        # self.tempo_division = 4
        self.beat_position = 0
        self.height = H
        self.width = bars*4
        self.max_beat_division = 8
        self.scale = scale
        self.octave = octave  # Starting octave
        self.max_num_instruments = MAX_INSTRUMENTS
        self.instruments = [Instrument(x, self.mport, key=key, scale=scale, octave=octave, speed=1, bars=bars) for x in range(MAX_INSTRUMENTS)]  # limit to 16 midi channels
        self.current_visible_instrument = 0
        # If we're loading, ignore all this and overwrite with info from file!
        if saved:
            self.load(saved)

    def add_notes_from_midi(self, notes):
        '''Take midi notes 48-74 inclusive, map to current grid'''
        # Map white keys to sequential numbers
        white_key_lookup = { v:k for k,v in enumerate([1,3,5,6,8,10,12,13,15,17,18,20,22,24,25,27]) }
        for note in notes:
            note = white_key_lookup.get(note-47)
            if note == None:  # Ugh, 0 is valid but falsey!
                continue
            self.get_curr_instrument().touch_note(self.get_curr_instrument().local_beat_position, note)
        return

    def change_division(self, up_down):
        '''Find current instrument, inc or dec its beat division as appropriate'''
        self.get_curr_instrument().change_division(up_down)
        return

    def cycle_key(self, up_down):
        '''Find current key in master list, move on to prev/next key, set in all modal instruments'''
        curr_key = KEYS.index(self.key)
        new_key = (curr_key + up_down) % len(KEYS)
        self.key = KEYS[new_key]
        for i in self.instruments:
            i.set_key(self.key)
        return

    def cycle_scale(self, up_down):
        '''Find current scale in master list, move on to prev/next key, set in all modal instruments'''
        curr_scale = list(SCALES.keys()).index(self.scale)
        new_scale = (curr_scale + up_down) % len(SCALES.keys())
        self.scale = list(SCALES.keys())[new_scale]
        for i in self.instruments:
            if not i.isdrum:
                i.set_scale(self.scale)
        return

    def change_octave(self, up_down):
        '''Find current key in master list, move on to prev/next key, set in all modal instruments'''
        self.get_curr_instrument().change_octave(up_down)
        return

    def swap_drum_inst(self):
        '''Swap the currently selected instrument between drum and instrument modes'''
        ins = self.get_curr_instrument()
        if ins.isdrum:
            ins.octave = self.octave
            ins.set_scale(self.scale)
            ins.isdrum = False
        else:
            ins.octave = 1
            ins.set_scale('chromatic')
            ins.isdrum = True

        return

    def get_status(self):
        status = {
            'ins_num': self.get_curr_instrument_num(),
            'ins_total': self.get_total_instrument_num(),
            'page_num': self.get_curr_instrument().curr_page_num+1,
            'page_total': len(self.get_curr_instrument().pages),
            'repeat_num': self.get_curr_instrument().curr_rept_num+1,
            'repeat_total': self.get_curr_instrument().get_curr_page().repeats,
            'page_stats': self.get_curr_instrument().get_page_stats(),
            'key': str(self.key),
            'scale': str(self.scale),
            'octave': str(self.get_curr_instrument().octave),
            'isdrum': self.get_curr_instrument().isdrum,
            'division': self.get_curr_instrument().get_beat_division_str(),
        }
        return status
    # def inc_tempo(self, amt):
    #     self.tempo += amt
    #     return
    #
    # def dec_tempo(self, amt):
    #     self.tempo -= amt
    #     return

    def add_instrument(self, key=None, scale=None, octave=2, bars=int(W/4), height=H):
        if not scale:
            scale = self.scale
        if not key:
            key = self.key
        if len(self.instruments) == 16:
            # logging.warning('Already at 16 instruments')
            return False
        ins_num = len(self.instruments)
        self.instruments.append(Instrument(ins_num, self.mport, key, scale, octave, bars, height))
        return

    def next_instrument(self):
        if self.current_visible_instrument == len(self.instruments)-1:
            # logging.warning('Reached end of instruments')
            return False
        self.current_visible_instrument += 1
        return

    def prev_instrument(self):
        if self.current_visible_instrument == 0:
            # logging.warning('Reached start of instruments')
            return False
        self.current_visible_instrument -= 1
        return

    def inc_rep(self, page):
        ins = self.get_curr_instrument()
        ins.inc_page_repeats(page)
        pass

    def dec_rep(self, page):
        ins = self.get_curr_instrument()
        ins.dec_page_repeats(page)
        pass

    def add_page(self):
        ins = self.get_curr_instrument()
        ins.add_page()
        pass


    def step_beat(self):
        self.beat_position += 1
        self.beat_position %= self.width * self.max_beat_division
        for ins in self.instruments:
            # ins.step_beat()#self.beat_position)
            ins.step_beat(self.beat_position)
        pass

    def get_curr_instrument(self):
        return self.instruments[self.current_visible_instrument]

    def get_curr_instrument_num(self):
        return self.current_visible_instrument + 1

    def get_total_instrument_num(self):
        return len(self.instruments)

    def touch_note(self, x, y):
        self.get_curr_instrument().touch_note(x, y)

    def get_led_grid(self):
        '''Get led status types for all cells of the grid, to be drawn by the display'''
        note_grid = self.get_curr_instrument().get_curr_page_grid()
        led_grid = []
        for c, column in enumerate(note_grid):  # columnn counter
            led_grid.append([self.get_led_status(x, c) for x in column])
        return led_grid

    def get_led_status(self, cell, beat_pos):
        '''Determine which type of LED should be shown for a given cell'''
        led = LED_BLANK  # Start with blank / no led
        if beat_pos == self.get_curr_instrument().local_beat_position:
            led = LED_BEAT  # If we're on the beat, we'll want to show the beat marker
            if cell == NOTE_ON:
                led = LED_SELECT  # Unless we want a selected + beat cell to be special
        elif cell == NOTE_ON:
            led = LED_ACTIVE  # Otherwise if the cell is active (touched)
        return led

    def save(self):
        return {
            "Height": 16,
            "Width": 16,
            "Instruments": [i.save() for i in self.instruments]
        }

    def load(self, saved):
        self.height = saved['Height']
        self.width = saved['Width']
        self.scale = saved['Instruments'][0]['Scale']
        self.octave = saved['Instruments'][0]['Octave']
        self.key = saved['Instruments'][0]['Key']
        for i in range(len(saved['Instruments'])):
            self.instruments[i].load(saved['Instruments'][i])

    # def draw(self, scr):
    #     note_grid = self.get_curr_instrument().get_curr_page_grid()
    #     for c, column in enumerate(note_grid):  # row counter
    #         for r, cell in enumerate(column):  # column counter
    #             led = self.get_led_status(cell, c)
    #             scr.addstr(H-r-1, c*2, DISPLAY[led])#, curses.color_pair(4))
    #     return


import unittest
class TestInstrument(unittest.TestCase):
    def test_instrument_nums(self):
        seq = Sequencer(None)
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        self.assertEqual(seq.get_total_instrument_num(), 1)
        seq.next_instrument()
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        seq.prev_instrument()
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        seq.prev_instrument()
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        seq.add_instrument("e", "major")
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        self.assertEqual(seq.get_total_instrument_num(), 2)
        seq.next_instrument()
        self.assertEqual(seq.get_curr_instrument_num(), 2)
        seq.prev_instrument()
        self.assertEqual(seq.get_curr_instrument_num(), 1)

    def test_multi_instrument_notes(self):
        seq = Sequencer(None)
        seq.add_instrument("e", "major")
        seq.touch_note(0,3)
        seq.touch_note(1,4)
        self.assertEqual(seq.get_curr_instrument_num(), 1)
        self.assertEqual(seq.get_curr_instrument().get_curr_notes(), [3])
        seq.next_instrument()
        seq.touch_note(0,5)
        seq.touch_note(1,6)
        self.assertEqual(seq.get_curr_instrument_num(), 2)
        self.assertEqual(seq.get_curr_instrument().get_curr_notes(), [5])
        seq.step_beat()
        self.assertEqual(seq.get_curr_instrument().get_curr_notes(), [6])
        seq.prev_instrument()
        self.assertEqual(seq.get_curr_instrument().get_curr_notes(), [4])

    def test_led_grid(self):
        seq = Sequencer(None)
        seq.touch_note(2,3)
        seq.touch_note(2,4)
        seq.touch_note(2,5)
        seq.touch_note(3,3)
        seq.touch_note(4,3)
        seq.step_beat()
        seq.step_beat()
        seq.step_beat()  # step to 4th beat, #3
        grid = seq.get_led_grid()
        print(grid)
        self.assertEqual(grid[0], [0,0,0,0,0,0,0,0,             0,0,0,0,0,0,0,0])
        self.assertEqual(grid[1], [0,0,0,0,0,0,0,0,             0,0,0,0,0,0,0,0])
        self.assertEqual(grid[2], [0,0,0,LED_ACTIVE,LED_ACTIVE,LED_ACTIVE,0,0, 0,0,0,0,0,0,0,0])
        self.assertEqual(grid[3], [LED_BEAT,LED_BEAT,LED_BEAT,LED_ACTIVE,LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT, LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT,LED_BEAT])
        self.assertEqual(grid[4], [0,0,0,LED_ACTIVE,0,0,0,0,     0,0,0,0,0,0,0,0])

if __name__ == '__main__':
    unittest.main()
