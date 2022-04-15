from user import User
from application import TextGenerator
from application import Statistics
from application import TimeOutFunction
import textwrap


class Application:
    def __init__(self, words_count: int, user: User):
        self.mistakes = 0
        self.user = user
        self.text = TextGenerator.TextGenerator(words_count).get_random_words()

    def run_app(self):
        self.show_text()
        user_words = []
        if self.user.os_name == "Windows":
            user_input = TimeOutFunction.TimeoutFunction(timeout=30).timed_input(
                "\nLets Go\n"
            )
            user_words = self.parse_to_world(user_input)
        stat = Statistics.Statistics(user_words, self.text)
        stat.find_mistakes()
        print(stat)

    def parse_to_world(self, user_input):
        SPECIAL_BYTES = b"\x08"
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

    def show_text(self):
        formatted = textwrap.fill(" ".join(self.text), width=50, initial_indent="" * 10)
        print(formatted)
