import curses

screen = curses.initscr()
#curses.noecho()
curses.curs_set(0)
screen.keypad(1)
curses.mousemask(1)

screen.addstr("This is a Sample Curses Script\n\n")

while True:
    event = screen.getch()
    if event == ord("q"):
        screen.addstr(20, 10, "Q")
    if event == curses.KEY_MOUSE:
        a = curses.getmouse()
        screen.addstr(20, 10, a)
    screen.refresh()

curses.endwin()
