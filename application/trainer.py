from typing import List, NoReturn
from user import User, UserState
from application import text_generator, wIndow_tools, keys
import time
import curses
from textwrap import fill

STRING_LENGTH = 50


class Trainer(wIndow_tools.WindowTools):
    def __init__(
            self, user: User, text_gen: text_generator.TextGenerator, word_count: int
    ) -> NoReturn:
        self.user = user
        self.user.state = UserState.State.PLAYING
        self.text_generator = text_gen
        self.text = self.text_generator.get_random_words(word_count)
        self.average_word_length = text_gen.get_average_word_length()

    @staticmethod
    def get_wrapper_position(formatted: str) -> List[int]:
        """Возвращает позицци, на которых был произведен перенос строки.


        Ключевые аргументы:
        formatted -- отформатированный текст
        """
        symbols_list = list(formatted)
        wrap_positions = []
        for i in range(len(symbols_list)):
            if symbols_list[i] == "\n":
                wrap_positions.append(i)
        return wrap_positions

    def display_text(
            self, stdscr: curses, current: List[str], wpm: int, accuracy: float, key
    ) -> NoReturn:
        """Отображает на экран исходный текст, текущий символ, wpm,точность набора и подчеркивает ошибку.


        Ключевые аргументы:
        stdscr -- главное окно\n
        current -- текущий текст\n
        wpm -- текущая скорость набора\n
        accuracy -- текущая точность набора
        """
        text = " ".join(self.text)
        formatted = fill(text, width=STRING_LENGTH)
        stdscr.addstr(formatted)

        current_wrap = 0
        incorrect_char = None
        wrap, wrap_positions = self.wrap_init(current_wrap, formatted, text)
        stdscr.addstr(len(wrap_positions) + 2, 0, f"WPM:{wpm}")
        stdscr.addstr(len(wrap_positions) + 3, 0, f"accuracy:{accuracy}")
        for i, char in enumerate(current):
            correct_char = text[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2)
                incorrect_char = char
            if i > wrap:
                stdscr.addstr(current_wrap + 1, i - wrap - 1, char, color)
                if current_wrap < len(wrap_positions) - 1:
                    if i == wrap_positions[current_wrap + 1]:
                        wrap = wrap_positions[current_wrap + 1]
                        current_wrap += 1
            else:
                stdscr.addstr(0, i, char, color)
        if incorrect_char and key not in keys.SPECIAL_SYMBOLS:
            self.user.mistakes.append(incorrect_char)

        return

    def wrap_init(self, current_wrap: int, formatted: str, text: str):
        """Инициализация списка переноса строк и начального индекса переноса строки.


        Ключевые аргументы:
        current_wrap -- текущее индекс переноса строки\n
        formatted -- отформатированный текст\n
        text - исходный текст
        """
        if len(text) > STRING_LENGTH:
            wrap_positions = self.get_wrapper_position(formatted)
            wrap = wrap_positions[current_wrap]
        else:
            wrap_positions = [0]
            wrap = STRING_LENGTH + 1
        return wrap, wrap_positions

    def wpm_test(self, stdscr: curses) -> NoReturn:
        """Вычисление скорости набора текста.


        Ключевые аргументы:
        stdscr -- главное окно
        """
        raw_current_text = []
        key = None
        start_time = time.time()
        text = " ".join(self.text)
        while self.user.state == UserState.State.PLAYING:
            time_elapsed = max(time.time() - start_time, 1)
            self.user.wpm = self.calculate_wpm(
                raw_current_text, time_elapsed, self.average_word_length
            )
            self.user.accuracy = self.calculate_accuracy(self.user.mistakes, text)
            stdscr.clear()
            self.display_text(
                stdscr, raw_current_text, self.user.wpm, self.user.accuracy, key
            )
            stdscr.refresh()
            current_text = "".join(raw_current_text)
            if current_text == text:
                stdscr.nodelay(False)
                break
            try:
                key = stdscr.get_wch()
            except curses.error:
                raise Exception("something wrong:(")
            while key == curses.KEY_RESIZE:
                key = stdscr.get_wch()
                self.redraw_window(stdscr)
                self.display_text(
                    stdscr, raw_current_text, self.user.wpm, self.user.accuracy, key
                )
            if type(key) is str and key == keys.EXIT_KEY:
                break
            elif type(key) is str and ord(key) == keys.EXIT_KEY:
                break
            if key in keys.SPECIAL_SYMBOLS and len(raw_current_text) > 0:
                raw_current_text.pop()
            elif len(current_text) < len(text):
                raw_current_text.append(key)

    def redraw_window(self, stdscr: curses) -> NoReturn:
        """Перерисовка окна


        Ключевые аргументы:
        stdscr -- главное окно"""
        stdscr.clear()
        stdscr.refresh()

    def init_window(self, stdscr: curses) -> NoReturn:
        """Инициализация окна


        Ключевые аргументы:
        stdscr -- главное окно
        """
        stdscr.clear()
        stdscr.refresh()

    @staticmethod
    def calculate_wpm(
            current_text: List[str], time_elapsed: float, average_word_length: float
    ) -> int:
        """Вычисление значения скорости набора текста.


        Ключевые аргументы:
        current_text -- текущий текст\n
        time_elapsed -- время в сек, прошедшее с начала набора
        """
        return round((len(current_text) / (time_elapsed / 60)) / average_word_length)

    @staticmethod
    def calculate_accuracy(mistakes: List[str], text: str) -> float:
        """Вычисление точности набора текста.


        Ключевые аргументы:
        mistakes -- количествно неправильных символов\n
        text -- исходный текст
        """
        return round((1 - (len(mistakes) / (len(text)))) * 100, 2)
