from abc import ABC, abstractmethod
import curses


class WindowTools(ABC):

    @abstractmethod
    def init_window(self, stdscr):
        pass

    @abstractmethod
    def redraw_window(self, stdscr):
        pass
