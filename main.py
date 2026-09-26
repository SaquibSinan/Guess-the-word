from word_manager import WordManager
from word_validator import WordValidator
from game_state import GameState
from game_engine import GameEngine
from offline_scoring import OfflineScoring
from offline_progress import OfflineProgress

def StartGame(progress,selected_level):
    if not progress.can_play(selected_level):
        print("This Level is Locked")
        return
    word_manager=WordManager()
    validator=WordValidator()
    word_data=word_manager.get_random_word(selected_level)
    game_state=GameState(word_data,selected_level)
    game_engine=GameEngine(game_state,validator)
    return game_engine

def main():
    progress = OfflineProgress()
    print("Welcome to Guess-the-Word")
    selected_level=int(input("Enter Level: "))
    game_engine=StartGame(progress,selected_level)
    if game_engine is None:
        return
    while not game_engine.state.won and not game_engine.state.forfeited:
        print("Word Length:", game_engine.state.length)
        guess=input("Enter Your Guess: ")
        result=game_engine.make_guess(guess)
        print(result)

        if game_engine.state.won or game_engine.state.forfeited:
            break

        if result["status"]=="invalid":
            continue
        if game_engine.clue_available():
            use_clue=input("Do you want to use a clue? (y/n): ")
            if use_clue.lower()=="y":
                clue=game_engine.give_clue()
                print(clue)
                continue
            elif use_clue.lower()=="n":
                game_engine.state.incorrect_attempts=0
        if game_engine.state.hints_used>=game_engine.state.max_hints and game_engine.state.incorrect_attempts>=5:
            use_forfeit=input("Do you want to forfeit?(y/n): ")
            if use_forfeit.lower()=="y":
                result=game_engine.forfeit()
                print(result)
                break
            elif use_forfeit.lower()=="n":
                game_engine.state.incorrect_attempts=0

    scoring=OfflineScoring(game_engine.state.level)
    points=scoring.calculate_points(game_engine.state)
    progress.add_points(points)

    print("Points Achieved:",points)
    print("Total Points:",progress.points)
    print("Highest Unlocked Level:",progress.level)

if __name__=="__main__":
    main()