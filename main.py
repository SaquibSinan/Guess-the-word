from word_manager import WordManager
from word_validator import WordValidator
from game_state import GameState
from game_engine import GameEngine
from offline_scoring import OfflineScoring
from offline_progress import OfflineProgress

def show_main_menu(progress):
print("\n========================")
print("     GUESS THE WORD")
print("========================")
print()
print("Points:", progress.points)
print("Highest Level:", progress.level)
print()
print("1. Play Offline")
print("2. View Progress")
print("3. Rules")
print("4. Exit")

def show_progress(progress):
print("\n========================")
print("      YOUR PROGRESS")
print("========================")
print()
print("Total Points:", progress.points)
print("Highest Unlocked Level:", progress.level)
print()
print("Unlocked Levels:")

```
for level in range(1, 8):
    if progress.can_play(level):
        print("✓ Level", level)
    else:
        print("✗ Level", level)

if progress.level < 7:
    next_level = progress.level + 1

    thresholds = {
        2: 500,
        3: 1200,
        4: 2000,
        5: 3000,
        6: 4200,
        7: 5500
    }

    required_points = thresholds[next_level]
    points_needed = required_points - progress.points

    print()
    print("Next Unlock: Level", next_level)
    print("Required Points:", required_points)
    print("Points Needed:", max(0, points_needed))
else:
    print()
    print("All levels are unlocked!")

input("\nPress Enter to return to the main menu.")
```

def show_rules():
print("\n========================")
print("        GAME RULES")
print("========================")
print()
print("1. Choose any unlocked level to play.")
print()
print("2. Enter a valid word of the correct length")
print("   to make a guess.")
print()
print("3. Invalid words do not count as attempts.")
print()
print("4. Letters in the correct position are revealed.")
print()
print("5. Letters that are in the word but in the")
print("   wrong position are marked as present.")
print()
print("6. A clue becomes available after 5 incorrect")
print("   attempts.")
print()
print("7. Using a clue reveals one unrevealed letter")
print("   and reduces the points earned for the round.")
print()
print("8. Each level has a limited number of clues.")
print()
print("9. Winning a round gives you points.")
print()
print("10. Forfeiting a round deducts points.")

```
input("\nPress Enter to return to the main menu.")
```

def choose_level(progress):
while True:
print("\n========================")
print("      CHOOSE LEVEL")
print("========================")
print()

```
    for level in range(1, 8):
        if progress.can_play(level):
            print(level, ". Level", level)
        else:
            print(level, ". Locked")

    print("0. Back to Main Menu")

    choice = input("\nChoose a level: ")

    if not choice.isdigit():
        print("Please enter a valid level number.")
        continue

    level = int(choice)

    if level == 0:
        return None

    if level < 1 or level > 7:
        print("Please choose a level from 1 to 7.")
        continue

    if not progress.can_play(level):
        print("You have not unlocked that level yet.")
        continue

    return level
```

def show_word(game_state):
print("\nWord:")

```
for i in range(game_state.length):
    if game_state.revealed[i]:
        print(game_state.word[i], end=" ")
    else:
        print("_", end=" ")

print()
```

def play_round(level, word_manager, validator, progress):
word_data = word_manager.get_random_word(level)

```
game_state = GameState(word_data, level)
game_engine = GameEngine(game_state, validator)
scoring = OfflineScoring(level)

print("\n========================")
print("        NEW ROUND")
print("========================")
print()
print("Level:", level)
print("Word Length:", game_state.length)

while not game_state.won and not game_state.forfeited:

    show_word(game_state)

    print()
    print("Incorrect Attempts:", game_state.incorrect_attempts)
    print("Hints Used:", game_state.hints_used, "/", game_state.max_hints)

    if game_engine.clue_available():
        print("A clue is available!")
        print("Type 'hint' to use it.")

    print("Type 'forfeit' to give up the round.")

    guess = input("\nEnter your guess: ")
    command = guess.strip().lower()

    if command == "hint":
        result = game_engine.give_clue()

        if result["status"] == "hint":
            print("\nHint revealed:", result["letter"])

        elif result["status"] == "won":
            print("\nThe final letter was revealed!")
            print("You completed the word!")

        else:
            print(result["message"])

        continue

    if command == "forfeit":
        result = game_engine.forfeit()

        if result["status"] == "forfeited":
            print("\nYou forfeited the round.")
            print("The word was:", result["word"])

        continue

    result = game_engine.make_guess(guess)

    if result["status"] == "invalid":
        print("\n" + result["message"])
        continue

    if result["status"] == "won":
        print("\nYou won the round!")
        break

    print("\nCorrect position:", result["correct_position"])
    print("Present but wrong position:", result["wrong_position"])
    print("Not present:", result["not_present"])

points = scoring.calculate_points(game_state)
progress.add_points(points)

print("\n========================")
print("      ROUND COMPLETE")
print("========================")

if game_state.won:
    print("You earned:", points, "points.")
elif game_state.forfeited:
    print("You lost:", abs(points), "points.")

print("Total Points:", progress.points)
print("Highest Unlocked Level:", progress.level)

if game_state.won:
    while True:
        print()
        print("1. Next Round")
        print("2. Main Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":
            return "next_round"

        if choice == "2":
            return "main_menu"

        print("Please choose 1 or 2.")

return "main_menu"
```

def main():
word_manager = WordManager()
validator = WordValidator()
progress = OfflineProgress()

```
print("\nWelcome to Guess the Word!")

while True:

    show_main_menu(progress)

    choice = input("\nChoose an option: ")

    if choice == "1":

        level = choose_level(progress)

        if level is None:
            continue

        while True:
            result = play_round(
                level,
                word_manager,
                validator,
                progress
            )

            if result == "main_menu":
                break

            if result == "next_round":
                continue

    elif choice == "2":
        show_progress(progress)

    elif choice == "3":
        show_rules()

    elif choice == "4":
        print("\nThanks for playing!")
        break

    else:
        print("\nPlease choose a valid option.")
```

if **name** == "**main**":
main()
