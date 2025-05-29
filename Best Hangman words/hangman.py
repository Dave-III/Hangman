import random
import utils
import wordSolver

GAME_VALID = ["1", "game", "hangman game", "hangman", "g"]
SOLVER_VALID = ["2", "solver", "hangman solver", "solve", "s"]
EXIT_VALID = ["3", "exit", "e"]

class HangmanSession:

    def __init__(self):
        self.wordToGuess = ''
        self.wordState = None
        with open(utils.WORDLIST_PATH) as wordFile:
            self.wordlist = wordFile.read().splitlines()

        self.selectWord()

    def selectWord(self):
        self.wordToGuess = random.choice(self.wordlist)
        self.wordState = "_" * len(self.wordToGuess)

    def reset(self):
        pass

    def main(self):
        loopFlag = True
        while loopFlag:
            print(f"Current word state: {self.wordState}")
            userInput = input("Select:\n[Guess Letter] [Restart] [Exit]\n>>> ")
            if userInput.lower() == "g":
                userLetter = utils.askUntilValid("Letter to guess:\n>>> ", list("abcdefghijklmnopqrstuvwxyz"))
                self.wordState = ''.join([userLetter if self.wordToGuess[index] == userLetter else self.wordState[index] for index in range(len(self.wordToGuess))])
            elif userInput.lower() == "r":
                print(self.wordToGuess)
            elif userInput.lower() == "e":
                loopFlag = False

if __name__ == "__main__":
    userIn = utils.askUntilValid("[1] Hangman Game\n[2] Hangman Solver\n[3] Exit\n>>> ", GAME_VALID + SOLVER_VALID + EXIT_VALID)
    if userIn.lower() in GAME_VALID:
        q = HangmanSession()
        q.main()
    elif userIn.lower() in SOLVER_VALID:
        while True:
            try:
                wordLength = int(input("What is the word length?\n>>> "))
            except ValueError:
                continue
            break
        solver = wordSolver.HangmanSolver(wordLength)
        solver.start()
    else:
        pass