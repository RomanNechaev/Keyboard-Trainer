from abc import ABC, abstractmethod


class WindowTools(ABC):
    """Интерфейс для окон, обязывает классы реализовать перерисовку окон и инициализацию окна """

    @abstractmethod
    def init_window(self, stdscr):
        pass

    @abstractmethod
    def redraw_window(self, stdscr):
        pass
