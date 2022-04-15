import re
import random

NOT_WORLD_PATTERN = r"[-:,.!?;{}\d(,)]"
MAX_WORD_COUNT = 20


class TextGenerator:
    def __init__(self, word_count):
        self.word_count = word_count

    @staticmethod
    def parse_text():
        with open("konstitucia-rf.txt", encoding="utf-8") as f, open(
            "kons.txt", "w"
        ) as fw:
            line = f.readline()
            while line:
                s = line.split()
                for word in s:
                    if re.search(NOT_WORLD_PATTERN, word) is None and len(word) > 2:
                        fw.write(word.lower() + "\n")
                line = f.readline()

    def get_random_words(self):
        with open("kons.txt", "rb") as f:
            result = []
            try:
                f.seek(-10, 2)
                end_file = f.tell() + 1
                rnd_position = random.randint(1, end_file)
                f.seek(rnd_position)
            except Exception:
                raise Exception("asdsd")
            for i in range(1, self.word_count):
                word = f.readline().decode("cp1251").replace("\r\n", "")
                result.append(word)
        result.remove(result[0])
        random.shuffle(result)
        return result
