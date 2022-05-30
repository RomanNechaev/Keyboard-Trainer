import curses
from user import User
from application import MenuTitles
from application import WIndowTools
import client
from application import KEYS


class Menu(WIndowTools.WindowTools):
    def __init__(self, user: User, trainer):
        self.user = user
        self.trainer = trainer
        self.client = client.Client(user, trainer)

    def init_window(self, stdscr):
        stdscr.clear()
        curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)
        window_size = stdscr.getmaxyx()
        x = window_size[1] // 2 - len(MenuTitles.MenuTitles.SINGLE_PLAY.value) // 2
        y = window_size[0] // 2

        stdscr.addstr(y - 2, x + 5,
                      MenuTitles.MenuTitles.MENU.value, curses.color_pair(10)
                      )
        stdscr.addstr(window_size[0] - 8, x,
                      MenuTitles.MenuTitles.SINGLE_PLAY.value, curses.color_pair(10)
                      )
        stdscr.addstr(window_size[0] - 6, x,
                      MenuTitles.MenuTitles.MULTIPLAYER.value, curses.color_pair(10)
                      )
        stdscr.addstr(window_size[0] - 4, x,
                      MenuTitles.MenuTitles.SETTINGS.value, curses.color_pair(10)
                      )
        stdscr.addstr(window_size[0] - 2, x,
                      MenuTitles.MenuTitles.STAT.value, curses.color_pair(10)
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

    def choice_game_type(self, key, stdscr):
        # try:
        if key in KEYS.KEY_O:
            self.trainer.wpm_test(stdscr)
        elif key in KEYS.KEY_G:
            self.trainer.text = self.trainer.text_generator.get_random_words(20)
            self.client.run_client(stdscr)

    # elif key in
    # except Exception:
    #     raise Exception("something wrong:(")

    def redraw_window(self, stdscr):
        stdscr.clear()
        window_size = stdscr.getmaxyx()
        coordinate_menu_x = window_size[1] // 2 - len(MenuTitles.MenuTitles.SINGLE_PLAY.value) // 2 + 5
        coordinate_menu_y = window_size[0] // 2 - 2
        y = window_size[0]
        stdscr.addstr(coordinate_menu_y, coordinate_menu_x,
                      MenuTitles.MenuTitles.MENU.value, curses.color_pair(10)
                      )
        stdscr.addstr(y - 8, coordinate_menu_x - 5,
                      MenuTitles.MenuTitles.SINGLE_PLAY.value, curses.color_pair(10)
                      )
        stdscr.addstr(y - 6, coordinate_menu_x - 5,
                      MenuTitles.MenuTitles.MULTIPLAYER.value, curses.color_pair(10)
                      )
        stdscr.addstr(y - 4, coordinate_menu_x - 5,
                      MenuTitles.MenuTitles.SETTINGS.value, curses.color_pair(10)
                      )
        stdscr.addstr(y - 2, coordinate_menu_x - 5,
                      MenuTitles.MenuTitles.STAT.value, curses.color_pair(10)
                      )

        stdscr.refresh()

    # TODO: Добавить логику меню(настройки, выбор типа игры и др)
    # TODO: В настройках можно выбирать тип переноса курсора(с пробелом и без)
    # TODO: добавить настройки, статистику, многопользовательский режим
