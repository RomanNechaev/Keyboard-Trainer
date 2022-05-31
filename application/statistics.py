class Statistics:
    def __init__(self, user_words, text):
        self.user_words = user_words
        self.text = text
        self.mistakes = 0
        self.incorrect_words = []

    def __str__(self):
        return (
            f"\n Your result is {len(self.user_words) - self.mistakes} WPM \n"
            f" You have a {self.mistakes} mistakes \n"
            f" Incorrect words: {' '.join(self.incorrect_words)}"
        )

    def find_mistakes(self):
        for t in range(len(self.user_words)):
            if not self.text.__contains__(self.user_words[t]):
                self.mistakes += 1
                self.incorrect_words.append(self.user_words[t])
