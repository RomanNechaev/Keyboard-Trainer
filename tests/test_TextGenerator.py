from application import text_generator
import unittest
import random
import re


class TextGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.text_gen = text_generator.TextGenerator("konstitucia-rf.txt")
        self.text_gen.parse_text()

    def test_only_words_in_file(self):
        NOT_WORLD_PATTERN = r"[-:,.!?;{}\d(,)]"
        with open("res.txt", "r") as f:
            line = f.readline()
            while line:
                res = re.findall(NOT_WORLD_PATTERN, line)
                self.assertEqual(len(res), 0)
                line = f.readline()

    def test_get_correct_random_length(self):
        rnd_count = random.randint(1, 100)
        text_gen2 = text_generator.TextGenerator("tests/test.txt")
        words = text_gen2.get_random_words(rnd_count)
        self.assertEqual(len(words), rnd_count)

    def test_generate_different_words_sequence(self):
        first_words_sequence = self.text_gen.get_random_words(10)
        second_words_sequence = self.text_gen.get_random_words(10)
        difference = None
        for i in range(10):
            if first_words_sequence[i] != second_words_sequence:
                difference = first_words_sequence[i]
        self.assertIsNotNone(difference)

    # def test_raise_error_if_words_count_equal_zero(self):
    #     text_gen = TextGenerator.TextGenerator(-1, "../konstitucia-rf.txt")
    #     self.assertRaises(IndexError, text_gen.get_random_words())

    def test_calculate_average_word_length_if_all_words_are_same_length(self):
        text_with_same_words = "tests/same_words.txt"
        length = self.text_gen.get_average_word_length(text_with_same_words)
        self.assertEqual(6.0, length)

    # def test_calculate_if_empty_file(self):
    #     self.assertRaises(ZeroDivisionError, self.text_gen.get_average_word_length("empty.txt"))

    def test_correct_calculate_average_words_length(self):
        self.assertEqual(4.0, self.text_gen.get_average_word_length("tests/words.txt"))

    def test_initialization_class(self):
        file_name = "konstitucia-rf.txt"
        test_text_gen = text_generator.TextGenerator(file_name)
        self.assertEqual(file_name, test_text_gen.file_name)
