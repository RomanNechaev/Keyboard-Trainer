import curses
from typing import NoReturn
from user import User
from application import menu_titles, wIndow_tools, keys
from multiplayer import client


class Menu(wIndow_tools.WindowTools):
    """Представляет собой графический интерфейс, который обрабытывает клавиши пользователя и
     переноправляет на соответсвующие окна"""

    def __init__(self, user: User, trainer) -> NoReturn:
        self.user = user
        self.trainer = trainer
        self.client = client.Client(user, trainer)

    def init_window(self, stdscr) -> NoReturn:
        """Инициализация окна меню


        Ключевые аргументы:
        stdscr -- главное окно
        """
        stdscr.clear()
        curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)
        window_size = stdscr.getmaxyx()
        x = window_size[1] // 2 - len(menu_titles.MenuTitles.SINGLE_PLAY.value) // 2
        y = window_size[0] // 2

        stdscr.addstr(
            y - 2, x + 5, menu_titles.MenuTitles.MENU.value, curses.color_pair(10)
        )
        stdscr.addstr(
            window_size[0] - 8,
            x,
            menu_titles.MenuTitles.SINGLE_PLAY.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            window_size[0] - 6,
            x,
            menu_titles.MenuTitles.MULTIPLAYER.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            window_size[0] - 4,
            x,
            menu_titles.MenuTitles.SETTINGS.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            window_size[0] - 2,
            x,
            menu_titles.MenuTitles.STAT.value,
            curses.color_pair(10),
        )

        try:
            key = stdscr.get_wch()
        except Exception:
            raise Exception("что-то пошло не так:(")
        while key == curses.KEY_RESIZE:
            key = stdscr.get_wch()
            self.redraw_window(stdscr)
        self.choice_game_type(key, stdscr)
        stdscr.refresh()

    def choice_game_type(self, key, stdscr) -> NoReturn:
        """Выбор режима игры/приложения в зависимости от клавиши


        Ключевые аргументы:
        key -- клавиша пользователя\n
        stdscr -- главное окно
        """
        if key in keys.KEY_O:
            self.trainer.wpm_test(stdscr)
        elif key in keys.KEY_G:
            self.trainer.text = self.trainer.text_generator.get_random_words(5)
            self.client.run_client(stdscr)

    def redraw_window(self, stdscr) -> NoReturn:
        """Перерисовка окна


        Ключевые аргументы:
        stdscr -- главное окно
        """
        stdscr.clear()
        window_size = stdscr.getmaxyx()
        coordinate_menu_x = (
                window_size[1] // 2 - len(menu_titles.MenuTitles.SINGLE_PLAY.value) // 2 + 5
        )
        coordinate_menu_y = window_size[0] // 2 - 2
        y = window_size[0]
        stdscr.addstr(
            coordinate_menu_y,
            coordinate_menu_x,
            menu_titles.MenuTitles.MENU.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            y - 8,
            coordinate_menu_x - 5,
            menu_titles.MenuTitles.SINGLE_PLAY.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            y - 6,
            coordinate_menu_x - 5,
            menu_titles.MenuTitles.MULTIPLAYER.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            y - 4,
            coordinate_menu_x - 5,
            menu_titles.MenuTitles.SETTINGS.value,
            curses.color_pair(10),
        )
        stdscr.addstr(
            y - 2,
            coordinate_menu_x - 5,
            menu_titles.MenuTitles.STAT.value,
            curses.color_pair(10),
        )
        stdscr.refresh()
