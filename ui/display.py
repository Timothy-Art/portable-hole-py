import curses
import curses.ascii
from enum import IntEnum

from ui.components import Element

MIN_HEIGHT = 50
MIN_WIDTH = 120


class Style(IntEnum):
    DEFAULT = 1
    HIGHLIGHT = 2
    MAGIC = 3

    @staticmethod
    def init_styles():
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)


class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.h, self.w = 0, 0
        self.idx = 0
        self.elements: dict = {}

        self.stdscr.clear()
        self.check_size()
        Style.init_styles()
        curses.curs_set(0)

        self.stdscr.refresh()

        while True:
            key = self.stdscr.getkey()

            self.stdscr.clear()
            self.stdscr.addstr(15, 10, key)

            if key == 'q':
                break

            self.stdscr.refresh()

    def check_size(self):
        self.h, self.w = self.stdscr.getmaxyx()
        if self.h < MIN_HEIGHT:
            self.h = MIN_HEIGHT
        if self.w < MIN_WIDTH:
            self.w = MIN_WIDTH
        self.resize(self.h, self.w)

    def resize(self, h, w):
        self.stdscr.resize(h, w)
        self.h, self.w = h, w
        curses.resize_term(self.h, self.w)

    def handle_elements(self):
        for element in self.elements.items():
            element.handle(self.stdscr)

    def draw_elements(self):
        for element in self.elements.items():
            element.draw(self.stdscr)

    def register(self, element: Element):
        self.elements[self.idx] = element
        self.idx += 1
        return self.idx - 1

    def deregister(self, element_idx):
        return self.elements.pop(element_idx)


curses.wrapper(Display)


