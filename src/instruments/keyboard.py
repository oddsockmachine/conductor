# coding=utf-8
from instruments.instrument import Instrument
import constants as c
import note_conversion as n
import mido
from collections import namedtuple
from buses import midi_out_bus

Key = namedtuple('Key', 'letter number sprite')


class Keyboard(Instrument):
    """Keyboard
    - Choose between 3 types of keyboard
    - Piano: white and black keys along 2x rows, octaves up y. Highlight scale keys?
    -  x x  x x x_____
    - o x xx x x xo___
    - Scalar: Only show keys in scale, highlight root, octaves along y
    - oxxxxxxoxxxxxx__
    - Isomorphic: isomorphic/hex grid
    - Fretboard/linnstrument, hightlight scale + root keys
    """

    def __init__(self, ins_num, mport, key, scale, octave=1, speed=1):
        super(Keyboard, self).__init__(ins_num, mport, key, scale, octave, speed)
        self.type = "Keyboard"
        self.height = 16
        self.width = 16
        self.layout = "piano"
        self.available_layouts = ['piano', 'scalar', 'iso', 'guitar']
        self.cached_keys = (None, [])
        self.set_layout(self.layout)
        self.new_notes = []

    def set_key(self, key):
        c.logging.info("new key, regen layout")
        self.key = key
        self.set_layout(self.layout)
        return

    def set_scale(self, scale):
        c.logging.info("new scale, regen layout")
        self.scale = scale
        self.set_layout(self.layout)
        return

    def set_layout(self, layout):
        if layout not in self.available_layouts:
            return
        self.layout = layout
        if layout == 'piano':
            self.cached_keys = ('piano', rotate_grid(create_piano_grid(self.scale, self.key)))
        if layout == 'guitar':
            self.cached_keys = ('guitar', rotate_grid(create_guitar_grid(self.scale, self.key)))
        if layout == 'scalar':
            self.cached_keys = ('scalar', rotate_grid(create_scalar_grid(self.scale, self.key)))
        if layout == 'iso':
            self.cached_keys = ('iso', rotate_grid(create_iso_grid(self.scale, self.key)))
        return

    def get_status(self):
        status = {
            'ins_num': self.ins_num+1,
            'ins_total': 16,
            'page_num': 0,
            'page_total': 0,
            'repeat_num': 0,
            'repeat_total': 0,
            'page_stats': {},
            'key': str(self.key),
            'scale': str(self.scale),
            'octave': str(self.octave),
            'type': self.type,
            'division': self.get_beat_division_str(),
            'random_rpt': False,
            'sustain': False,
        }
        return status

    def touch_note(self, state, x, y):
        '''touch the x/y cell on the current page'''
        if y < 14:
            key = self.cached_keys[1][x][y]
            c.logging.info(key.number)
            self.new_notes.append(key.number)
        elif y == 15:
            layout = {6+i: self.available_layouts[i] for i in range(len(self.available_layouts))}.get(x)
            if layout:
                self.set_layout(layout)
        return True

    def keys_to_led_grid(self, keys):
        grid = [[None for x in range(c.W)] for y in range(c.H)]
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                grid[y][x] = key.sprite
        # add buttons over top
        for i in range(len(self.available_layouts)):
            grid[6+i][15] = c.SLIDER_BODY
        grid[6+(self.available_layouts.index(self.layout))][15] = c.SLIDER_TOP
        return grid

    def get_led_grid(self, state):
        return self.keys_to_led_grid(self.cached_keys[1])

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            return
        self.local_beat_position = local
        self.output(self.old_notes, self.new_notes)
        self.old_notes = self.new_notes
        return

    def output(self, notes_off, notes_on):
        """Return all note-ons from the current beat, and all note-offs from the last"""
        notes_off = [n for n in notes_off if n < 128 and n > 0]
        notes_on = [n for n in notes_on if n < 128 and n > 0]
        off_msgs = [mido.Message('note_off', note=n, channel=self.ins_num) for n in notes_off]
        on_msgs = [mido.Message('note_on', note=n, channel=self.ins_num) for n in notes_on]
        msgs = off_msgs + on_msgs
        if len(msgs) > 0:
            c.debug(msgs)
            midi_out_bus.put(msgs)

    def save(self):
        saved = {
          "layout": self.layout,
        }
        saved.update(self.default_save_info())
        return saved

    def load(self, saved):
        self.load_default_info(saved)
        self.layout = saved["layout"]
        return

    def clear_page(self):
        return


class Key(object):
    """docstring for Key."""

    def __init__(self, number, sprite):
        super(Key, self).__init__()
        self.letter = n.midi_to_letter(number)
        self.number = number
        self.sprite = sprite

    def __repr__(self):
        # return str(self.letter)
        return c.DISPLAY[self.sprite]


def get_keys_for_scale(row_scale, starting_note, rotate, length, scale, key, b_w):
    keys = []
    scale_notes = n.create_cell_to_midi_note_lookup(scale, -1, key, 62).values()
    scale = n.SCALE_INTERVALS[row_scale]
    for interval in scale:
        keys.append(1)
        for gap in range(interval-1):
            keys.append(0)
    if rotate:
        keys = keys[rotate:] + keys[:rotate]
    while (len(keys) < length):
        keys.extend(keys)
    for i, k in enumerate(keys):
        if k == 1:
            keys[i] = i + starting_note+1
    for i, k in enumerate(keys):
        if k in scale_notes:
            keys[i] = Key(k, c.KEY_SCALE)
        elif k == 0:
            keys[i] = Key(0, c.LED_BLANK)
        else:
            keys[i] = Key(k, c.KEY_WHITE if b_w == 'w' else c.KEY_BLACK)
    return keys[:length]


def create_piano_grid(scale, key):
    grid = []
    grid.append([Key(0, c.LED_BLANK) for x in range(c.W)])
    grid.append([Key(0, c.LED_BLANK) for x in range(c.W)])
    offset = 23
    for h in range(int((c.H-1)/2))[::-1]:
        w_keys = get_keys_for_scale('major', (h * 12) + offset, 0, c.W, scale, key, 'w')
        b_keys = get_keys_for_scale('pentatonic_maj', (h * 12) + offset, 6, c.W, scale, key, 'b')
        grid.append(b_keys)
        grid.append(w_keys)
    while (len(grid) < c.W):
        grid.extend([[Key(0, c.LED_BLANK) for x in range(c.W)]])
    return grid



def create_scalar_grid(scale, key):
    keys = []
    scale_notes = list(n.create_cell_to_midi_note_lookup(scale, -1, key, 62).values())
    root_notes = list(scale_notes)[::(5 if 'penta' in scale else 7)]
    for octave, y in enumerate(range(7)):
        keys.append(list(n.create_cell_to_midi_note_lookup(scale, octave, key, c.W).values()))
    grid = []
    for x in range(5):
        grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    for row in keys[::-1]:
        grid.append([Key(k, c.KEY_ROOT if (n in root_notes) else c.KEY_SCALE) for i, k in enumerate(row)])
    for x in range(4):
        grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    return grid


def create_iso_grid(scale, key):
    keys = []
    scale_notes = list(n.create_cell_to_midi_note_lookup(scale, -1, key, 62).values())
    root_notes = list(scale_notes)[::(5 if 'penta' in scale else 7)]
    for octave, y in enumerate(range(7)):
        keys.append([Key(n, c.KEY_ROOT if (n in root_notes) else c.KEY_SCALE)
                     for n in scale_notes[5+(5*octave):5+(5*octave)+c.W]])
    grid = []
    for x in range(5):
        grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    for row in keys[::-1]:
        grid.append(row)
    for x in range(4):
        grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    return grid


def create_guitar_grid(scale, key):
    scale_notes = n.create_cell_to_midi_note_lookup(scale, -1, key, 62).values()
    root_notes = list(scale_notes)[::(5 if 'penta' in scale else 7)]
    start = 21 + n.KEYS.index(key)
    grid = []
    for i, r in enumerate(range(c.H-2)):
        row = []
        for x in range(c.W):
            note = start + x
            sprite = c.KEY_SCALE if note in scale_notes else c.KEY_WHITE
            if note in root_notes:
                sprite = c.KEY_ROOT
            row.append(Key(note, sprite))
        start += 5
        grid.append(row)
    grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    return grid[::-1]


def rotate_grid(keys):
    grid = [[None for x in range(c.W)] for y in range(c.H)]
    for y, row in enumerate(keys):
        for x, key in enumerate(row):
            grid[x][c.H-y-1] = key
    return grid
