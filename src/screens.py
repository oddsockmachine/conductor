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
        ('key_dec', args['key'][0], 5, 0),
        ('key_inc', args['key'][1], 5, 4),
        ('load', 'l', 11, 0),
        ('save', 's', 11, 4),
        ('instrument_sel', NUM_INSTRUMENTS[args['num_instruments']], 0, 15),
        # ('instrument_type', args['num_instrument_types'], 14, 0),
    ]
    return gbl_cfg

def generate_screen(defn, args):
    defn = defn(args)
    led_grid = empty_grid()
    callback_grid = empty_grid()
    for cb, char, x, y in defn:
        if type(char) == str:
            char = LETTERS[char]
        else:
            char = char
        led_grid = add_char_to_grid(led_grid, char, x, y)
        callback_grid = add_callback_to_grid(callback_grid, char, cb, x, y)
    return rotate_grid(led_grid), rotate_grid(callback_grid)

def create_gbl_cfg_grid(instruments, key, scale):
    grid = []
    for x in range(16):
        grid.append([LED_BLANK for y in range(16)])
    # Scale
    scale_chars = SCALE_CHARS[scale]
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
            # logging.info('i' + str(i))
            # logging.info('j' + str(j))
            # logging.info('x' + str(x))
            # logging.info('m' + str(m))
            # logging.info('y' + str(y))
            # logging.info('n' + str(n))
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

# pprint(create_gbl_cfg_grid([0,2,4,6,8,9,10], 'b#', 'mixolydian'))
# led, cb = generate_screen(gbl_cfg_grid_defn, {'scale_chars': 'ab', 'key':'c#'})
# from pprint import pprint
# pprint(led)
# pprint(cb)
# print(get_cb_from_touch(cb, 0,15))
# led, cb = generate_screen(gbl_cfg_grid_defn, {'scale_chars': 'ab', 'key':'c#'})
# print(get_cb_from_touch(cb, 0,15))
