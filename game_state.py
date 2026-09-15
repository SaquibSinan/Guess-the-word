class GameState:
    def __init__(self,word_data,level):
        self.word=word_data["word"].lower()
        self.length=int(word_data["Length"])
        self.level=level

        self.revealed=[False]*self.length

        self.incorrect_attempts=0
        self.total_attempts=0

        self.won=False
        self.forfeited=False

    def revealed_count(self):
        return sum(self.revealed)
    def maximum_revealed_count(self):
        return round(0.4*self.length)
    def remaining_reveal_capacity(self):
        return int(self.maximum_revealed_count()-self.revealed_count())
    def reveal_all(self):
        self.revealed=[True]*self.length