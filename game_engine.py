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
                "correct_position": list(range(1,self.state.length+1)),
                "wrong_position": [],
                "not_present": [],
                "Total Attempts":self.state.total_attempts
            }

        correct_position = []
        wrong_position = []
        not_present = []

        remaining_letters = list(self.state.word)

        for i in range(self.state.length):
            if guess[i] == self.state.word[i]:
                correct_position.append(i+1)
                self.state.revealed[i] = True
                remaining_letters[i] = None

        for i in range(self.state.length):
            if (i+1) in correct_position:
                continue

            if guess[i] in remaining_letters:
                wrong_position.append(i+1)

                letter_index = remaining_letters.index(guess[i])
                remaining_letters[letter_index] = None
            else:
                not_present.append(i+1)
        
        self.state.incorrect_attempts += 1

        return {
            "status": "wrong",
            "correct_position": correct_position,
            "wrong_position": wrong_position,
            "not_present": not_present
        }

    def clue_available(self):
        return self.state.clue_available()

    def give_clue(self):

        if not self.state.clue_available():
            return {
                "status": "unavailable",
                "message": "A clue is not available."
            }

        unrevealed_positions = [
            i
            for i in range(self.state.length)
            if not self.state.revealed[i]
        ]

        if not unrevealed_positions:
            return {
                "status": "unavailable",
                "message": "All letters have already been revealed."
            }

        position = random.choice(unrevealed_positions)

        self.state.use_hint()
        self.state.revealed[position] = True

        return {
            "status": "hint",
            "position": position+1,
            "letter": self.state.word[position]
        }

    def forfeit(self):
        if not self.state.can_forfeit():
            return {
            "status": "unavailable",
            "message": "Forfeit is not available yet."
            }
        self.state.reveal_all()
        self.state.forfeited = True

        return {
            "status": "forfeited",
            "word": self.state.word
        }