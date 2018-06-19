import sys,os
import curses
from time import sleep

def get_m(stdscr):
    while True:
        stdscr.clear()
        stdscr.refresh()
        # id, x, y, z, bstate = curses.getmouse()
        # print(id, x, y, z, bstate)
        sleep(1)
        # output = "id {}   x {}   y {}   z {}   bstate {}".format(id, x, y, z, bstate)
        output = "hi"
        stdscr.addstr(5,5, output)
        # screen_y, screen_x, clip_h, clip_w = self.clip_size()
            # y -= screen_y
            # x -= screen_x

            # Ignore clicks outside clipped screen
            # if y < clip_h and x < clip_w:
            #     return self.mouse_target(screen, y, x)


def main():
    curses.wrapper(get_m)

if __name__ == "__main__":
    main()
