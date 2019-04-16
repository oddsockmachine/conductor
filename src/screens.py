from constants import *
# from instruments import instrument_lookup
total_num_instruments = 10

def get_char(**kwargs):
    '''Return a char bitmap as array, looked up from inputs'''
    # logging.info(str(kwargs))
    if 'char' in kwargs.keys():
        array = LETTERS.get(kwargs['char'])
    elif 'row' in kwargs.keys():
        array = [ROW[0][:kwargs['row']]]
        if 'selector' in kwargs.keys():
            array[0][kwargs['selector']] = LED_SELECT
    elif 'column' in kwargs.keys():
        array = COLUMN[:kwargs['column']]
        if 'selector' in kwargs.keys():
            array[kwargs['selector']] = [LED_SELECT]
    elif 'instrument' in kwargs.keys():
        array = COLUMN[:kwargs['instrument']]
        if 'selector' in kwargs.keys():
            array[kwargs['selector']] = [LED_SELECT]
    elif 'clips' in kwargs.keys():
        array = [[0 for x in range(4)] for y in range(4)]
        pages = kwargs['clips']
        for p in range(pages):
            y, x = (p % 4, int(p / 4))
            array[x][y] = LED_CURSOR
        if 'curr_page' in kwargs.keys():
            y, x = (kwargs['curr_page'] % 4, int(kwargs['curr_page'] / 4))
            array[x][y] = LED_SELECT
        if 'next_page' in kwargs.keys():
            y, x = (kwargs['next_page'] % 4, int(kwargs['next_page'] / 4))
            array[x][y] = LED_ACTIVE
    elif 'pages' in kwargs.keys():
        max_rpts = 8
        max_pages = 16
        array = [[0 for x in range(max_rpts)] for y in range(max_pages)]
        for i, rpts in enumerate(kwargs['pages']):
            for r in range(rpts):
                array[i][r] = LED_ACTIVE
        c_r, c_p = kwargs['active']
        array[c_r][c_p] = LED_SELECT
    return array

def empty_grid():
    grid = []
    for x in range(16):
        grid.append([LED_BLANK for y in range(16)])
    return grid

def seq_cfg_grid_defn(args):
    seqcfg = [
        ('sustain', get_char(char='s'), 0, 9),
        ('random_pages', get_char(char='r'), 0, 13),
        ('speed', get_char(row=5, selector=args['speed']), 15, 11),
        ('octave', get_char(row=5, selector=args['octave']), 14, 11),
        ('page', get_char(active=args['curr_p_r'], pages=args['pages']), 0, 0),
        ('clip', get_char(clips=len(args['pages']), curr_page=args['curr_page'], next_page=args['next_page']), 9, 9),
    ]
    return seqcfg

def dev_cfg_grid_defn(args):
    devcfg = [
        ('random_pages', get_char(char='r'), 0, 13),
        ('speed', get_char(row=5, selector=args['speed']), 15, 11),
        ('octave', get_char(row=5, selector=args['octave']), 14, 11),
        ('page', get_char(active=args['curr_p_r'], pages=args['pages']), 0, 0),
        ('clip', get_char(clips=len(args['pages']), curr_page=args['curr_page'], next_page=args['next_page']), 9, 9),
    ]
    return devcfg

def oct_cfg_grid_defn(args):
    octcfg = [
        ('random_pages', get_char(char='r'), 0, 13),
        ('copy_page', get_char(char='c'), 0, 9),
        ('speed', get_char(row=5, selector=args['speed']), 15, 11),
        ('octave', get_char(row=5, selector=args['octave']), 14, 11),
        ('page', get_char(active=args['curr_p_r'], pages=args['pages']), 0, 0),
        ('clip', get_char(clips=len(args['pages']), curr_page=args['curr_page'], next_page=args['next_page']), 9, 9),
    ]
    return octcfg

def drum_cfg_grid_defn(args):
    drumcfg = [
        ('random_pages', get_char(char='r'), 0, 13),
        ('speed', get_char(row=5, selector=args['speed']), 15, 11),
        ('octave', get_char(row=5, selector=args['octave']), 14, 11),
        ('page', get_char(active=args['curr_p_r'], pages=args['pages']), 0, 0),
        ('clip', get_char(clips=len(args['pages']), curr_page=args['curr_page'], next_page=args['next_page']), 9, 9),
    ]
    return drumcfg

def gbl_cfg_grid_defn(args):
    gbl_cfg = [
        ('scale_dec', get_char(char=args['scale_chars'][0]), 0, 0),
        ('scale_inc', get_char(char=args['scale_chars'][1]), 0, 4),
        ('key_dec', get_char(char=args['key'][0]), 5, 0),
        ('key_inc', get_char(char=args['key'][1]), 5, 4),
        ('load', get_char(char='l'), 11, 0),
        ('save', get_char(char='s'), 11, 4),
        ('reset', get_char(char='x'), 11, 8),
        ('instrument_sel', get_char(instrument=args['num_ins'], selector=args['curr_ins']), 0, 15),
        ('instrument_type', get_char(instrument=total_num_instruments), 0, 14),  # TODO extend instrument adder, use diff colors for each
    ]
    return gbl_cfg

def generate_screen(defn, args):
    defn = defn(args)
    led_grid = empty_grid()
    callback_grid = empty_grid()
    for cb, char, x, y in defn:
        led_grid = add_char_to_grid(led_grid, char, x, y)
        callback_grid = add_callback_to_grid(callback_grid, char, cb, x, y)
    return rotate_grid(led_grid), rotate_grid(callback_grid)

def add_char_to_grid(grid, char, x, y, color=None):
    '''Overlay a char bitmap to an existing grid, starting at top left x,y'''
    for m, i in enumerate(char):
        for n, j in enumerate(i):
            if j == 0:
                continue
            grid[x+m][y+n] = j
            if color:
                pass  # TODO  overwrite with color
    return grid

def add_callback_to_grid(grid, char, cb, x, y):
    for m, i in enumerate(char):
        for n, j in enumerate(i):
            grid[x+m][y+n] = '_'.join([cb,str(m),str(n)])
    return grid

def rotate_grid(grid):
    '''Screen uses different coordinate system, rotate 90deg'''
    new_grid = grid[::-1]
    new_grid = list(zip(*new_grid))
    return new_grid

def get_cb_from_touch(cb_grid, x, y):
    cb = cb_grid[x][y]
    if cb == 0:
        return (None, None, None)
    cb_parts = cb.split('_')
    return '_'.join(cb_parts[:~1]), int(cb_parts[~0]), int(cb_parts[~1])   # (callback, x, y)  (x and y are swapped, as coordinates are rotated)

# led, cb = generate_screen(gbl_cfg_grid_defn, {'scale_chars': 'ab', 'key':'c#'})
# from pprint import pprint
# pprint(led)
# pprint(cb)
# print(get_cb_from_touch(cb, 0,15))
# led, cb = generate_screen(gbl_cfg_grid_defn, {'scale_chars': 'ab', 'key':'c#'})
# print(get_cb_from_touch(cb, 0,15))

import unittest
class TestChars(unittest.TestCase):
    def test_get_char(self):
        # seq = Conductor(None)
        self.assertEqual(get_char(char='s'), S)
        self.assertEqual(get_char(char='+'), PLUS)
        self.assertEqual(get_char(row=6), [1,1,1,1,1,1])
        self.assertEqual(get_char(column=5), [[1],[1],[1],[1],[1]])
        self.assertEqual(get_char(row=6, selector=2), [1,1,5,1,1,1])
        self.assertEqual(get_char(column=5, selector=2), [[1],[1],[5],[1],[1]])

if __name__ == '__main__':
    unittest.main()
