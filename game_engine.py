import random


class GameEngine:
    def __init__(self, game_state, validator):
        self.state = game_state
        self.validator = validator

    def make_guess(self, guess):
        guess = guess.strip().lower()

        if not self.validator.is_valid(guess, self.state.length):
            return {
                "status": "invalid",
                "message": "Invalid word or outside of the game's word list."
            }

        self.state.total_attempts += 1

        if guess == self.state.word:
            self.state.reveal_all()
            self.state.won = True

            return {
                "status": "won",
                "correct_position": list(range(self.state.length)),
                "wrong_position": [],
                "not_present": []
            }

        correct_position = []
        wrong_position = []
        not_present = []

        remaining_letters = list(self.state.word)

        for i in range(self.state.length):
            if guess[i] == self.state.word[i]:
                correct_position.append(i)
                self.state.revealed[i] = True
                remaining_letters[i] = None

        for i in range(self.state.length):
            if i in correct_position:
                continue

            if guess[i] in remaining_letters:
                wrong_position.append(i)

                letter_index = remaining_letters.index(guess[i])
                remaining_letters[letter_index] = None
            else:
                not_present.append(i)


        if correct_position:
            self.state.incorrect_attempts = 0
        else:
            self.state.incorrect_attempts += 1

        if self.state.revealed_count() == self.state.length:
            self.state.won = True

            return {
                "status": "won",
                "correct_position": correct_position,
                "wrong_position": wrong_position,
                "not_present": not_present
            }

        return {
            "status": "wrong",
            "correct_position": correct_position,
            "wrong_position": wrong_position,
            "not_present": not_present
        }

    def clue_available(self):
        return self.state.clue_available()

    def give_clue(self):
        if self.state.won or self.state.forfeited:
            return {
                "status": "unavailable",
                "message": "The round has already ended."
            }

        if not self.state.clue_available():
            return {
                "status": "unavailable",
                "message": "A clue is not available yet."
            }

        unrevealed_positions = [
            i
            for i in range(self.state.length)
            if not self.state.revealed[i]
        ]

        if not unrevealed_positions:
            self.state.won = True

            return {
                "status": "won",
                "message": "All letters have already been revealed."
            }

        if not self.state.use_hint():
            return {
                "status": "unavailable",
                "message": "No hint is available."
            }

        position = random.choice(unrevealed_positions)

        self.state.revealed[position] = True

        if self.state.revealed_count() == self.state.length:
            self.state.won = True

            return {
                "status": "won",
                "position": position,
                "letter": self.state.word[position]
            }

        return {
            "status": "hint",
            "position": position,
            "letter": self.state.word[position]
        }

    def forfeit(self):
        if self.state.won or self.state.forfeited:
            return {
                "status": "unavailable",
                "message": "The round has already ended."
            }

        self.state.reveal_all()
        self.state.forfeited = True

        return {
            "status": "forfeited",
            "word": self.state.word
        }
