from application import text_generator, trainer
from application import app
from application import trainer
from user import User, UserState
import unittest
from unittest.mock import MagicMock
from application import keys


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.text_gen = text_generator.TextGenerator("../konstitucia-rf.txt")
        user = User.User(UserState.State.PLAYING, "test")
        self.app = app.Application(user, self.text_gen, word_count=10)

    def test_correct_calculate_wpm(self):
        # 15 chr 30 sec -> 30 chr per min ->
        # 60/average_word_length(ex = 10), -> 3 per min
        time_elapsed = 30
        text = "a" * 15
        average_word_len = 10
        wpm = self.app.trainer.calculate_wpm(list(text), time_elapsed, average_word_len)
        self.assertEqual(3, wpm)

    def test_correct_calculate_wpm_if_one_word(self):
        time_elapsed = 30
        text = "a" * 5
        average_word_len = 10
        wpm = self.app.trainer.calculate_wpm(list(text), time_elapsed, average_word_len)
        self.assertEqual(1, wpm)

    def test_calculate_wpm_with_empty_text(self):
        time_elapsed = 30
        text = ""
        average_word_len = 10
        wpm = self.app.trainer.calculate_wpm(list(text), time_elapsed, average_word_len)
        self.assertEqual(0, wpm)

    def test_correct_calculate_mistakes_if_all_symbols_correct(self):
        stdscr = MagicMock(addsthr=MagicMock())
        correct_current_text = list(" ".join(self.app.trainer.text[:6]))
        with unittest.mock.patch("curses.color_pair"):
            self.app.trainer.display_text(
                stdscr,
                correct_current_text,
                wpm=MagicMock(),
                accuracy=MagicMock(),
                key=MagicMock(),
            )
            self.assertEqual(len(self.app.user.mistakes), 0)

    def test_correct_calculate_mistakes_if_one_mistakes(self):
        stdscr = MagicMock(addsthr=MagicMock())
        correct_current_text = list(" ".join(self.app.trainer.text[:6]))
        correct_current_text[3] = correct_current_text[3].upper()
        with unittest.mock.patch("curses.color_pair"):
            self.app.trainer.display_text(
                stdscr,
                correct_current_text,
                wpm=MagicMock(),
                accuracy=MagicMock(),
                key=MagicMock(),
            )
            self.assertEqual(len(self.app.user.mistakes), 1)

    def test_correct_calculate_mistakes_if_current_text_empty(self):
        stdscr = MagicMock(addsthr=MagicMock())
        correct_current_text = []
        with unittest.mock.patch("curses.color_pair"):
            self.app.trainer.display_text(
                stdscr,
                correct_current_text,
                wpm=MagicMock(),
                accuracy=MagicMock(),
                key=MagicMock(),
            )
            self.assertEqual(len(self.app.user.mistakes), 0)

    def test_correct_calculate_mistakes_if_several_symbols(self):
        stdscr = MagicMock(addsthr=MagicMock())
        correct_current_text_first = list(" ".join(self.app.trainer.text[:5]))
        correct_current_text_second = list(" ".join(self.app.trainer.text[:6]))
        correct_current_text_first[4] = correct_current_text_first[4].upper()
        correct_current_text_second[5] = correct_current_text_second[5].upper()
        with unittest.mock.patch("curses.color_pair"):
            self.app.trainer.display_text(
                stdscr,
                correct_current_text_first,
                wpm=MagicMock(),
                accuracy=MagicMock(),
                key=MagicMock(),
            )
            self.app.trainer.display_text(
                stdscr,
                correct_current_text_second,
                wpm=MagicMock(),
                accuracy=MagicMock(),
                key=MagicMock(),
            )
            self.assertEqual(len(self.app.user.mistakes), 2)

    def test_calculate_accuracy_if_zero_mistakes(self):
        mistakes = []
        accuracy = self.app.trainer.calculate_accuracy(mistakes, self.app.trainer.text)
        self.assertEqual(accuracy, 100.0)

    def test_correct_calculate_accuracy_if_all_current_text_incorrect(self):
        mistakes = [i for i in range(len(self.app.trainer.text))]
        accuracy = self.app.trainer.calculate_accuracy(mistakes, self.app.trainer.text)
        self.assertEqual(accuracy, 0)

    def test_correct_calculate_wrapper_position(self):
        text = "abrakadbra\n" "asdasd\n" "asd\n" "as\n"
        self.assertListEqual(
            [10, 17, 21, 24], self.app.trainer.get_wrapper_position(text)
        )

    def test_calculate_wrapper_position_if_not_line_wrapping(self):
        text = "abrakadbra"
        self.assertListEqual([], self.app.trainer.get_wrapper_position(text))

    def test_correct_initialization_wrap(self):
        # STRING_LENGTH DEFAULT = 50
        text = "a" * 30
        current_wrap = 0
        formatted = "aaaaaaaaaaaaaa\n" "aaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertTupleEqual(
            (51, [0]), self.app.trainer.wrap_init(current_wrap, formatted, text)
        )

    def test_correct_initialization_wrap_with_other_data(self):
        # STRING_LENGTH DEFAULT = 50
        text = "a" * 100
        current_wrap = 0
        formatted = "aaaaaaaaaaaaaa\n" "aaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertTupleEqual(
            (self.app.trainer.get_wrapper_position(formatted)[current_wrap],
             self.app.trainer.get_wrapper_position(formatted)),
            self.app.trainer.wrap_init(current_wrap, formatted, text)
        )

    def test_wpm_test_if_user_state_is_not_playing(self):
        stdscr = MagicMock(addstr=MagicMock())
        self.app.user.state = UserState.State.WAITING
        self.app.trainer.wpm_test(stdscr)
        self.assertEqual(self.app.user.wpm, 0)

    def test_initialization_class(self):
        user = User.User(UserState.State.WAITING, name="Vova")
        word_count = 12
        tr = trainer.Trainer(user, self.text_gen, word_count)
        tt = trainer.Trainer(user, self.text_gen, word_count)
        self.assertEqual(tr.user.name, tt.user.name)
        self.assertEqual(tr.text_generator, self.text_gen)
