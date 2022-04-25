from application import TextGenerator
import unittest
import random
import re


class TextGeneratorTests(unittest.TestCase):
    global text_gen
    text_gen = TextGenerator.TextGenerator(10, "test.txt")
    text_gen.parse_text()

    def test_only_words_in_file(self):
        NOT_WORLD_PATTERN = r"[-:,.!?;{}\d(,)]"
        with open("res.txt", "r") as f:
            line = f.readline()
            while line:
                self.assertEqual(re.search(NOT_WORLD_PATTERN, line), None)
                line = f.readline()

    def test_get_correct_random_length(self):
        rnd_count = random.randint(1, 100)
        text_gen2 = TextGenerator.TextGenerator(rnd_count, "test.txt")
        words = text_gen2.get_random_words()
        self.assertEqual(len(words), rnd_count)
