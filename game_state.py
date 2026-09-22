class GameState:
    def __init__(self, word_data, level):
        self.word = word_data["word"].lower()
        self.length = int(word_data["Length"])
        self.level = level

        self.revealed = [False] * self.length

        self.incorrect_attempts = 0
        self.total_attempts = 0

        self.hints_used = 0
        self.max_hints = self.get_max_hints()

        self.won = False
        self.forfeited = False

    def get_max_hints(self):
        if self.level in [1, 2]:
            return 2
        elif self.level in [3, 4]:
            return 3
        elif self.level in [5, 6]:
            return 4
        elif self.level == 7:
            return 5

        return 0

    def revealed_count(self):
        return sum(self.revealed)

    def clue_available(self):
        return (
            self.incorrect_attempts >= 5
            and self.hints_used < self.max_hints
        )

    def use_hint(self):
        if not self.clue_available():
            return False

        self.hints_used += 1
        self.incorrect_attempts = 0

        return True

    def reveal_all(self):
        self.revealed = [True] * self.length
