import random
import utils

GAME_VALID = ["1", "game", "hangman game", "hangman", "g"]
SOLVER_VALID = ["2", "solver", "hangman solver", "solve", "s"]

class HangmanSession:

    def __init__(self):
        self.wordToGuess = ''
        with open("words_alpha.txt") as wordFile:
            self.wordlist = wordFile.read().splitlines()

        self.selectWord()

    def selectWord(self):
        self.wordToGuess = random.choice(self.wordlist)

    def main(self):
        loopFlag = True
        while loopFlag:
            userInput = input("Select:\n[Guess Letter] [Restart] [Exit]\n>>> ")
            if userInput.lower() == "g":
                pass
            elif userInput.lower() == "r":
                print(self.wordToGuess)
            elif userInput.lower() == "e":
                loopFlag = False

if __name__ == "__main__":
    userIn = input("[1] Hangman Game\n[2] Hangman Solver\n[3] Exit\n>>> ")
    if userIn.lower() in GAME_VALID:
        q = HangmanSession()
        q.main()
    elif userIn.lower() in SOLVER_VALID:
        pass
    else:
        pass