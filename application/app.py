from typing import NoReturn
from user import User, UserState
from application import text_generator, trainer, menu, wIndow_tools, keys, app_consts
import curses
from curses import wrapper


class Application(wIndow_tools.WindowTools):
    def __init__(
            self, user: User, text_generator: text_generator, word_count: int
    ) -> NoReturn:
        self.user = user
        self.user.state = UserState.State.PLAYING
        self.text_generator = text_generator
        self.trainer = trainer.Trainer(user, text_generator, word_count)
        self.menu = menu.Menu(user, self.trainer)
        self.word_count = word_count

    def run_app(self) -> NoReturn:
        """Запустить приложение"""
        wrapper(self.main)

    def init_window(self, stdscr: curses) -> NoReturn:
        """Инициализация стартового окна.


        Ключевые аргументы:
        stdscr -- главное окно
        """
        stdscr.clear()
        stdscr.addstr(
            f"Привет,{self.user.name}! {app_consts.hello_message}"
        )
        stdscr.addstr(app_consts.press_any_key)
        try:
            key = stdscr.get_wch()
        except Exception:
            raise Exception("что-то пошло не так:(")
        while key == curses.KEY_RESIZE:
            key = stdscr.get_wch()
            self.redraw_window(stdscr)
        stdscr.refresh()

    def redraw_window(self, stdscr):
        stdscr.clear()
        stdscr.addstr(
            f"Привет,{self.user.name}! {app_consts.hello_message}"
        )
        stdscr.addstr(app_consts.press_any_key)
        stdscr.refresh()

    def main(self, stdscr: curses) -> NoReturn:
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.init_window(stdscr)
        self.menu.init_window(stdscr)
        while self.trainer.user.state == UserState.State.PLAYING:
            last_wrap_index = stdscr.getyx()[0]
            stdscr.addstr(
                last_wrap_index + 4,
                0,
                app_consts.start_again,
                curses.color_pair(5),
            )
            stdscr.addstr(
                last_wrap_index + 5,
                0,
                app_consts.to_menu,
                curses.color_pair(4),
            )
            try:
                key = stdscr.get_wch()
            except curses.error:
                raise Exception("something wrong:(")
            self.trainer.text = self.text_generator.get_random_words(
                word_count=self.word_count
            )
            self.trainer.user.mistakes = []
            while key == curses.KEY_RESIZE:
                key = stdscr.get_wch()
                stdscr.refresh()
            if type(key) is str and key == keys.EXIT_KEY:
                self.trainer.user.state = UserState.State.EXIT
                break
            elif type(key) is str and ord(key) == keys.EXIT_KEY:
                self.trainer.user.state = UserState.State.EXIT
                break
            elif type(key) is str and key in keys.MENU_KEY:
                self.menu.init_window(stdscr)
            elif type(key) is str and ord(key) in keys.MENU_KEY:
                self.menu.init_window(stdscr)
            else:
                self.trainer.wpm_test(stdscr)
            stdscr.refresh()
