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

from constants import *

def empty_grid():
    grid = []
    for x in range(16):
        grid.append([LED_BLANK for y in range(16)])
    return grid

def gbl_cfg_grid_defn(args):
    gbl_cfg = [
        ('scale_dec', args['scale_chars'][0], 0, 0),
        ('scale_inc', args['scale_chars'][1], 0, 4),
        ('key_inc', args['key'][0], 5, 0),
        ('key_dec', args['key'][1], 5, 4),
        ('load', 'l', 11, 0),
        ('save', 's', 11, 4),
        # ('instrument_sel', args['instruments'], 15, 0),
        # ('instrument_tyoe', args['instrument_types'], 14, 0),
    ]
    return gbl_cfg

def generate_screen(defn, args):
    defn = defn(args)
    led_grid = empty_grid()
    callback_grid = empty_grid()
    for item in defn:
        led_grid = add_char_to_grid(led_grid, LETTERS[item[1]], item[2], item[3])
        callback_grid = add_callback_to_grid(callback_grid, LETTERS[item[1]], item[0], item[2], item[3])
    return led_grid, callback_grid

def create_gbl_cfg_grid(instruments, key, scale):
    grid = []
    for x in range(16):
        grid.append([LED_BLANK for y in range(16)])
    # Scale
    scale_chars = SCALES[scale]
    grid = add_char_to_grid(grid, LETTERS[scale_chars[0]], 0, 0)
    grid = add_char_to_grid(grid, LETTERS[scale_chars[1]], 0, 4)
    # Key
    sharp = '#' in key
    key = key.replace('#','')
    grid = add_char_to_grid(grid, LETTERS[key], 5, 0)
    if sharp:
        grid = add_char_to_grid(grid, LETTERS['#'], 5, 4)
    # Load, Save
    grid = add_char_to_grid(grid, LETTERS['l'], 11, 0)
    grid = add_char_to_grid(grid, LETTERS['s'], 11, 4)
    # Instruments
    for i in instruments:
        grid[i][15] = 1
    for i in range(8):  # TODO dynamic lookup of different instruments, different colors
        grid[i][14] = 1
    return rotate_grid(grid)

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
            grid[x+m][y+n] = cb
    return grid

def rotate_grid(grid):
    '''Screen uses different coordinate system, rotate 90deg'''
    new_grid = grid[::-1]
    new_grid = list(zip(*new_grid))
    return new_grid

def get_cb_from_touch(cb_grid, x, y):
    cb_txt = cb_grid[x][y]
    return cb_txt

# pprint(create_gbl_cfg_grid([0,2,4,6,8,9,10], 'b#', 'mixolydian'))
led, cb = generate_screen(gbl_cfg_grid_defn, {'scale_chars': 'ab', 'key':'c#'})
from pprint import pprint
pprint(led)
pprint(cb)
