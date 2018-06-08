from constants import *

class Cursor(object):
    def __init__(self, w=W, h=H):
        self.x = 0
        self.y = 0
        self.visible = True
        self.width = w
        self.height = h

    def move(self, x, y):
        self.x += x
        self.y += y
        self.constrain()
        pass

    def constrain(self):
        self.x = max(0, self.x)
        self.x = min(W-1, self.x)
        self.y = max(0, self.y)
        self.y = min(H-1, self.y)
        return

    def make_visible(self, vis):
        if vis:
            self.visible = True
        else:
            self.visible = False
        return
    #
    # def draw(self, stdscr):
    #     stdscr.addstr(self.height-self.y-1, self.x*2, DISPLAY[LED_ACTIVE])#, curses.color_pair(4))
    #     return

    def get_pos(self):
        return {'x': self.x, 'y': self.y}
