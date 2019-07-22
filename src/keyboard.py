from pprint import pprint
import constants as c
# from collections import namedtuple
import note_conversion as n

# Key = namedtuple('Key', 'letter number sprite')


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
        # grid.append([Key(0, c.LED_BLANK) for x in range(c.W)])
        grid.append(b_keys)
        grid.append(w_keys)
    while (len(grid) < c.W):  # TODO put blank lines at top
        grid.extend([[Key(0, c.LED_BLANK) for x in range(c.W)]])
    return grid


def create_scalar_grid(scale, key):
    keys = []
    scale_notes = list(n.create_cell_to_midi_note_lookup(scale, -1, key, 62).values())
    root_notes = list(scale_notes)[::(5 if 'penta' in scale else 7)]
    for octave, y in enumerate(range(7)):
        # keys.append(list(n.create_cell_to_midi_note_lookup(scale, octave, key, c.W).values()))
        keys.append([Key(n, c.KEY_ROOT if (n in root_notes) else c.KEY_SCALE) for n in scale_notes[5+(5*octave):5+(5*octave)+c.W]])
    grid = []
    for x in range(5):
        grid.append([Key(0, c.LED_BLANK) for i in range(c.W)])
    for row in keys[::-1]:
        grid.append(row)
        # TODO lookup actual roots, as penta scales are %5 not %7
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


# pprint(create_piano_grid('pentatonic_maj', 'c'))
pprint(create_scalar_grid('dorian', 'a'))
# pprint(create_guitar_grid('pentatonic_maj', 'd'))

# TODO lookup/conversion between note number and note letter
# TODO for all notes in grid, x-ref w list of scale keys and list of root keys
