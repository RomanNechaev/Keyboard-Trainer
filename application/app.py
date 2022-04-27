from typing import List, NoReturn
from user import User, UserState
from application import TextGenerator
import time
import curses
from curses import wrapper
from textwrap import fill

SPECIAL_SYMBOLS = (263, "BS", "KEY_BACKSPACE", "\b", "\x7f")
EXIT_KEY = 27
STRING_LENGTH = 50


class Application:
    def __init__(self, words_count: int, user: User, file_name: str) -> NoReturn:
        self.words_count = words_count
        self.user = user
        self.user.state = UserState.State.PLAYING
        self.text = TextGenerator.TextGenerator(
            words_count, file_name
        ).get_random_words()
        self.file_name = file_name

    def run_app(self) -> NoReturn:
        wrapper(self.main)

    def start_screen(self, stdscr: curses) -> NoReturn:
        stdscr.clear()
        stdscr.addstr(
            f"Привет,{self.user.name}! Давай проверим твою скорость набора текста"
        )
        stdscr.addstr("\nНажми любую клавишу чтобы начать")
        stdscr.refresh()
        stdscr.getkey()

    def get_wrapper_position(self, formatted: str) -> List[int]:
        """Возвращает позицци, на которых был произведен перенос строки"""
        symbols_list = list(formatted)
        wrap_positions = []
        for i in range(len(symbols_list)):
            if symbols_list[i] == "\n":
                wrap_positions.append(i)
        return wrap_positions

    def display_text(
            self, stdscr: curses, current: List[str], wpm: int, accuracy: float
    ) -> NoReturn:
        """Отображает на экран исходный текст, текущий символ, wpm,точность набора и подчеркивает ошибку"""
        text = " ".join(self.text)
        formatted = fill(text, width=STRING_LENGTH)
        stdscr.addstr(formatted)
        current_wrap = 0
        if len(text) > STRING_LENGTH:
            wrap_positions = self.get_wrapper_position(formatted)
            wrap = wrap_positions[current_wrap]
        else:
            wrap_positions = [0]
            wrap = STRING_LENGTH + 1
        stdscr.addstr(len(wrap_positions) + 2, 0, f"WPM:{wpm}")
        stdscr.addstr(len(wrap_positions) + 3, 0, f"accuracy:{accuracy}")
        for i, char in enumerate(current):
            correct_char = text[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2)
                self.user.mistakes += 1
            if i > wrap:
                stdscr.addstr(current_wrap + 1, i - wrap - 1, char, color)
                if current_wrap < len(wrap_positions) - 1:
                    if i == wrap_positions[current_wrap + 1]:
                        wrap = wrap_positions[current_wrap + 1]
                        current_wrap += 1
            else:
                stdscr.addstr(0, i, char, color)

    def wpm_test(self, stdscr: curses) -> NoReturn:
        """Вычисление скорости набора текста"""
        raw_current_text = []
        start_time = time.time()
        stdscr.timeout(-100)
        text = " ".join(self.text)
        while self.user.state == UserState.State.PLAYING:
            time_elapsed = max(time.time() - start_time, 1)
            self.user.wpm = self.calculate_wpm(raw_current_text, time_elapsed)
            self.user.accuracy = self.calculate_accuracy(self.user.mistakes, text)
            stdscr.clear()
            self.display_text(
                stdscr, raw_current_text, self.user.wpm, self.user.accuracy
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
            if type(key) is str and key == EXIT_KEY:
                self.user.state = UserState.State.EXIT
                break
            elif type(key) is str and ord(key) == EXIT_KEY:
                self.user.state = UserState.State.EXIT
                break
            if key in SPECIAL_SYMBOLS and len(raw_current_text) > 0:
                raw_current_text.pop()
            elif len(current_text) < len(" ".join(self.text)):
                raw_current_text.append(key)

    def calculate_wpm(self, current_text: List[str], time_elapsed: float) -> int:
        """Вычисление значения скорости набора"""
        return round((len(current_text) / (time_elapsed / 60)) / 5)

    def calculate_accuracy(self, mistakes: int, text: str) -> float:
        """Вычисление точности набора"""
        return round((1 - (mistakes / (len(text)))) * 100, 2)

    def main(self, stdscr: curses) -> NoReturn:
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.start_screen(stdscr)

        while self.user.state == UserState.State.PLAYING:
            self.wpm_test(stdscr)
            stdscr.addstr(2, 0, "Нажими любую клавишу чтобы начать снова...")
            try:
                key = stdscr.get_wch()
            except curses.error:
                raise Exception("something wrong:(")
            self.text = TextGenerator.TextGenerator(
                self.words_count, self.file_name
            ).get_random_words()
            self.user.mistakes = 0
            if type(key) is str and key == EXIT_KEY:
                self.user.state = UserState.State.EXIT
                break
            elif type(key) is str and ord(key) == EXIT_KEY:
                self.user.state = UserState.State.EXIT
                break
