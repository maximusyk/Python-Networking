"""
      1 - Send message to the server and print it with sended time.
      2 - Send message to the server, which repeat this message after 5 sec.
      3 - Send few message to the server; Server can stop
      connections after command.
      4 - Server with few connections.
      5 - Server with nonblocking mode.
"""
import curses
import os
import time


menu = ['First Task', 'Second Task', 'Exit']


def firstTask(stdscr):
    stdscr.clear()
    stdscr.refresh()
    print("It's First Task")
    os.system("new >> python3 tcp-client.py")
    # time.sleep(5)


def secondTask(stdscr):
    stdscr.clear()
    stdscr.refresh()
    print("It's Second Task")
    time.sleep(5)


def printMenu(stdscr, selectedRowIdx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2-len(row)//2
        y = h//2-len(menu)//2+idx
        if idx == selectedRowIdx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    crntRowIdx = 0

    printMenu(stdscr, crntRowIdx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and crntRowIdx > 0:
            crntRowIdx -= 1
        elif key == curses.KEY_DOWN and crntRowIdx < len(menu)-1:
            crntRowIdx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if crntRowIdx == len(menu)-1:
                break
            elif crntRowIdx == 0:
                firstTask(stdscr)
            else:
                secondTask(stdscr)

        printMenu(stdscr, crntRowIdx)
        stdscr.refresh()


curses.wrapper(main)
