# GBL_CFG_SCREEN
# SSSSSS____SS________________iiII
# SS__SS____SS________________iiII
# SSSSSS__SSSSSS______________iiII
# SS________SS________________iiII
# SS________SS________________iiII
# ____kk______________________iiII
# ____kk__kk__________________iiII
# kkkkkk__kkkk________________iiII
# kk__kk__kkkk________________iiII
# kkkkkk______________________iiII
# ____________________________iiII
# ##______######______________iiII
# ##______##__________________iiII
# ##______######______________iiII
# ##__________##______________iiII
# ######__######______________iiII
#
# L = Load
# s = Save
# I = Select instrument
# i = new instrument type
# S = Current scale (click left/right to inc/dec)
# k = Current key (click left/right to inc/dec)

# SSSSSS__RRRRRR______________PPPP
# SS______RR__RR______________PPPP
# SSSSSS__RRRR________________CCPP
# ____SS__RR__RR__________PPPPPPPP
# SSSSSS__RR__RR__________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# ________________________________
# OOOOOOoo________________________
# SSSSSSss________________________

# C curr_page_num
# C curr_rept_num
# R random_pages
# S sustain
# P pages
# o/O octave
# S/s speed



from constants import *

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
    elif 'pages' in kwargs.keys():
        max_rpt = 8
        array = [[0 for x in range(8)] for y in range(8)]
        for i, rpts in enumerate(kwargs['pages']):
            for r in range(rpts):
                array[i][r] = LED_ACTIVE
        c_r, c_p = kwargs['active']
        array[c_r][c_p] = LED_SELECT
    # logging.info(str(kwargs))
    # logging.info(str(array))
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
        ('speed', get_char(row=5, selector=args['speed']), 15, 0),
        ('octave', get_char(row=5, selector=args['octave']), 14, 0),
        ('page', get_char(active=args['curr_p_r'], pages=args['pages']), 0, 0),
    ]
    return seqcfg

def gbl_cfg_grid_defn(args):
    gbl_cfg = [
        ('scale_dec', get_char(char=args['scale_chars'][0]), 0, 0),
        ('scale_inc', get_char(char=args['scale_chars'][1]), 0, 4),
        ('key_dec', get_char(char=args['key'][0]), 5, 0),
        ('key_inc', get_char(char=args['key'][1]), 5, 4),
        ('load', get_char(char='l'), 11, 0),
        ('save', get_char(char='s'), 11, 4),
        ('instrument_sel', get_char(column=args['num_ins'], selector=args['curr_ins']), 0, 15),
        # ('instrument_type', args['num_instrument_types'], 14, 0),
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
    # logging.info(str(char))
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
    return '_'.join(cb_parts[:~1]), cb_parts[~0], cb_parts[~1]   # (callback, x, y)  (x and y are swapped, as coordinates are rotated)

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
