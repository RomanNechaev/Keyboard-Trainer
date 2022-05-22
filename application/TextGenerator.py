import re
import random
from dataclasses import dataclass
from typing import NoReturn, List

NOT_WORLD_PATTERN = r"[-:,.!?;{}\d(,)]"


@dataclass
class TextGenerator:
    """Генерирует рандомные слова из заданного текста"""

    word_count: int
    file_name: str

    def parse_text(self) -> NoReturn:
        """Парсинг исходного текста в файл со словами"""
        with open(self.file_name, encoding="utf-8") as f, open(
                "res.txt", "w", encoding="utf-8"
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
            try:
                result = []
                f.seek(-10, 2)
                end_file = f.tell() + 1
                rnd_position = random.randint(1, end_file)
                f.seek(rnd_position)
            except Exception:
                raise Exception("something wrong")
            for i in range(0, self.word_count + 1):
                word = f.readline().decode(errors="ignore").replace("\r\n", "")
                result.append(word)
        result.remove(result[0])
        random.shuffle(result)
        return result

    @staticmethod
    def get_average_word_length(filename="res.txt") -> float:
        """Возращает среднюю длину слова в тексте"""
        all_words_length = 0
        count = 0
        s = []
        with open(filename, "rb") as f:
            line = f.readline().decode(errors="ignore").replace("\r\n", "")
            while line:
                count += 1
                all_words_length += len(line)
                s.append(line)
                line = f.readline().decode(errors="ignore").replace("\r\n", "")
        return all_words_length / count
