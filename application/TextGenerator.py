import re
import random
from typing import NoReturn, List

NOT_WORLD_PATTERN = r"[-:,.!?;{}\d(,)]"
MAX_WORD_COUNT = 5


class TextGenerator:
    """Генерирует рандомные слова из заданного текста"""

    def __init__(self, word_count: int, filename: str):
        self.word_count = word_count
        self.file_name = filename

    def parse_text(self) -> NoReturn:
        """Парсинг исходного текста в файл со словами """
        with open(self.file_name, encoding="utf-8") as f, open(
                "../res.txt", "w"
        ) as fw:
            line = f.readline()
            while line:
                s = line.split()
                for word in s:
                    if re.search(NOT_WORLD_PATTERN, word) is None and len(word) > 2:
                        fw.write(word.lower() + "\n")
                line = f.readline()

    def get_random_words(self) -> List[str]:
        """Выдаёт рандомную последовательность слов"""
        with open("res.txt", "rb") as f:
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
