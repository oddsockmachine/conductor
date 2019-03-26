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
#
# Ionian     IO
# Dorian     DO
# Phrygian   PH
# Lydian     LY
# Mixolydian MX
# Aeolian    AE
# Locrian    LO
# Major      MA
# Minor      MI
# Penta Maj  P+
# Penta Min  P-
# Chromatic  CH

from constants import *
from pprint import pprint

def create_gbl_cfg_grid(instruments, scale, key):
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
    return grid

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

pprint(create_gbl_cfg_grid(None, 'mixolydian', 'b#'))
