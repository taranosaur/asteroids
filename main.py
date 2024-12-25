# main.py
from game import Game
from states import GameplayState

if __name__ == "__main__":
    game = Game(initial_state_class=GameplayState)
    game.run()
