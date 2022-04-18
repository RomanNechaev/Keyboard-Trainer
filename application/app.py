from user import User
from application import TextGenerator
from application import Statistics
import textwrap
import sys
import time
import msvcrt


class Application:
    def __init__(self, words_count: int, user: User):
        self.mistakes = 0
        self.user = user
        self.text = TextGenerator.TextGenerator(words_count).get_random_words()
        self.gen = self.get_generator()

    def run_app(self):
        self.show_text()
        user_words = []
        if self.user.os_name == "Windows":
            user_input = self.timed_input("\nLets Go\n", 30)
            user_words = self.parse_to_world(user_input)
        stat = Statistics.Statistics(user_words, self.text)
        stat.find_mistakes()
        print(stat)

    def words_for_parse(self):
        words = list(map(lambda x: x.__add__(" "), self.text))
        return words

    @staticmethod
    def parse_to_world(user_input):
        raw_input = user_input
        words = []
        word = []
        for i in range(len(raw_input)):
            if raw_input[i] != " ":
                word.append(raw_input[i])
            else:
                if raw_input[i - 1] != " ":
                    words.append("".join(word))
                    word = []
        return words

    def get_generator(self):
        words = self.words_for_parse()
        gen = (j for i in words for j in i)
        return gen

    def show_text(self):
        formatted = textwrap.fill(" ".join(self.text), width=50, initial_indent="" * 10)
        print(formatted)

    def timed_input(self, caption, timeout):
        def echo(c):
            sys.stdout.write(c)
            sys.stdout.flush()

        echo(caption)
        result = []
        start = time.monotonic()
        try:
            while time.monotonic() - start < timeout:
                if msvcrt.kbhit():
                    c = msvcrt.getwch()
                    if self.gen.__next__() != c:
                        print("->", end="")
                    if ord(c) == 13:
                        echo("\r\n")
                        break

                    result.append(str(c))
                    echo(c)
        except StopIteration:
            pass

        if result:
            return result
