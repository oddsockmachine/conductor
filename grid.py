#coding=utf-8
import copy
import curses
import locale
locale.setlocale(locale.LC_ALL, '')

# import curses
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)

LED_BLANK = 0
LED_SELECT = 1
LED_CURSOR = 2
LED_ACTIVE = 3
NOTE_OFF = 0
NOTE_ON = 3

CURR_PAGE = 0

w, h = 16, 16;
def create_grid(width, height):
    return [[1 for x in range(width)] for y in range(height)]

NOTE_GRID = {
    0: create_grid(w, h),
    1: create_grid(w, h),
    2: create_grid(w, h),
    3: create_grid(w, h),
}

def toggle_note(grid, page, x, y):
    state = grid[page][x][y]
    if state == NOTE_OFF:
        grid[page][x][y] = NOTE_OFF
    else:
        grid[page][x][y] = NOTE_ON
    return grid


NOTE_GRID = toggle_note(NOTE_GRID, CURR_PAGE, 0, 0)
NOTE_GRID = toggle_note(NOTE_GRID, CURR_PAGE, 1, 1)
NOTE_GRID = toggle_note(NOTE_GRID, CURR_PAGE, 2, 2)
NOTE_GRID = toggle_note(NOTE_GRID, CURR_PAGE, 3, 3)
NOTE_GRID = toggle_note(NOTE_GRID, CURR_PAGE, 4, 4)


def select_column(g, column):
    grid = copy.deepcopy(g)
    for r in range(len(grid[column])):
        cell = grid[r][column]
        if cell == LED_BLANK:
            grid[r][column] = LED_SELECT
        else:
            grid[r][column] = LED_CURSOR
    return grid

DISPLAY_GRID = [[LED_BLANK for x in range(w)] for y in range(h)]

def print_grid(g):
    display = {0: '. ', 1: '░░', 2:'▒▒', 3:'▓▓'}
    for x in g:
        for y in x:
            print(display[y]+''),
        print('')

def display_notes(notes, page):
    grid = copy.deepcopy(notes[page])
    return grid

print_grid(select_column(display_notes(NOTE_GRID, CURR_PAGE), 3))

class Note_Grid(object):
    def __init__(self, page_name, h, w):
        self.height = h
        self.width = w
        self.name = page_name
        self.note_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]

class Select_Grid(object):
    def __init__(self):
        self.rows_selected = []
        self.columns_selected = []

class Cursor_Grid(object):
    def __init__(self):
        self.x = -1
        self.y = -1

class Display(object):
    def __init__(self, h, w, scr):
        self.scr = scr
        self.height = h
        self.width = w
        self.display_grid = [[LED_BLANK for x in range(self.width)] for y in range(self.height)]
        self.current_page = 0
        # self.cursor = cursor
        # self.select = select
        # self.notes = notes
        self.k = 1
        self.cursor_x = 0
        self.cursor_y = 0


    def print_grid(self):
        display = {0: '. ', 1: '░░', 2:'▒▒', 3:'▓▓'}
        for x in self.display_grid:
            for y in x:
                print(display[y]+''),
            print('')

    def refresh(self):
        self.print_grid(select_column(display_notes(NOTE_GRID, CURR_PAGE), 3))

    def draw(self):
        # k = 0
        # cursor_x = 0
        # cursor_y = 0
        # while (k != ord('q')):
        self.k = self.scr.getch()
        if (self.k == ord('q')):
            return

        # Initialization
        self.scr.clear()
        height, width = 32, 48

        if self.k == curses.KEY_DOWN:
            self.cursor_y = self.cursor_y + 1
        elif self.k == curses.KEY_UP:
            self.cursor_y = self.cursor_y - 1
        elif self.k == curses.KEY_RIGHT:
            self.cursor_x = self.cursor_x + 3
        elif self.k == curses.KEY_LEFT:
            self.cursor_x = self.cursor_x - 3

        self.cursor_x = max(0, self.cursor_x)
        self.cursor_x = min(width-1, self.cursor_x)

        self.cursor_y = max(0, self.cursor_y)
        self.cursor_y = min(height-1, self.cursor_y)



        for x in range(0,48,3):
            for y in range(0,16,1):
                self.scr.addstr(y, x, '░░')
        # self.scr.move(self.cursor_y, self.cursor_x)
        self.scr.addstr(self.cursor_y, self.cursor_x, '▓▓')#, curses.color_pair(1))

        # Refresh the screen
        self.scr.refresh()

        # Wait for next input
        print(self.k)
        return self.k

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    display_grid = Display(16,16,stdscr)
    k = 0
    while (k != ord('q')):
        k = display_grid.draw()
    return


if __name__ == "__main__":
    curses.wrapper(main)
