
class Selector(object):
    def __init__(self):
        self.rows_selected = []
        self.columns_selected = []

class Cursor(object):
    def __init__(self):
        self.x = -1
        self.y = -1
        self.visible = True

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
        self.cursor = Cursor()
