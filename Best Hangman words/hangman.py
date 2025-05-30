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
        self.guessCount = 0
        self.guessedLetters = []

        with open(utils.WORDLIST_PATH) as wordFile:
            self.wordlist = wordFile.read().splitlines()

        self.selectWord()

    def selectWord(self):
        self.wordToGuess = random.choice(self.wordlist)
        self.wordState = "_" * len(self.wordToGuess)

    def showGuessed(self):
        print("Guessed Letters:")
        for counter, letter in enumerate(self.guessedLetters, start = 1):
            print(f"\t{utils.TerminalColours.applyColour((utils.TerminalColours.REG_GREEN if letter in self.wordToGuess else utils.TerminalColours.REG_RED), letter)}", end='')
            if (counter % 5 == 0):
                print()
        print()
      
    def reset(self):
        self.guessCount = 0
        self.guessedLetters = []
        self.selectWord()

    def endDialog(self):
        userIn = utils.askUntilValid("[New Word] [Exit]\n>>> ", EXIT_VALID + ["nw", "n", "new word", "new", "word"])
        if userIn in EXIT_VALID:
            return False
        else:
            utils.TerminalColours.printColour(utils.TerminalColours.BLD_CYAN, "---------- NEW GAME ----------")
            return True

    def main(self):
        loopFlag = True
        while loopFlag:
            print(f"Current Word State: {self.wordState}")
            self.showGuessed()
            userInput = input("Select:\n[Guess Letter] [Restart] [Back] [Exit]\n>>> ")
            if userInput.lower()[0] == "g":
                while True:
                    userLetter = input("Letter to guess:\n>>> ").lower()
                    if len(userLetter) != 1:
                        print("Error: Must input a single letter!")
                        continue
                    elif userLetter not in "abcdefghijklmnopqrstuvwyxz":
                        print("Error: Must not be a number or special character!")
                        continue
                    elif userLetter in self.guessedLetters:
                        print("Error: Letter has already been guessed!")
                        continue
                    break
                self.wordState = ''.join([userLetter.lower() if self.wordToGuess[index] == userLetter else self.wordState[index] for index in range(len(self.wordToGuess))])
                self.guessedLetters.append(userLetter)
                if self.wordState == self.wordToGuess:
                    print(f"You have guessed the word {self.wordToGuess} in {self.guessCount} guesses!\nOptimally, you could have guessed the word in {len(set(list(self.wordToGuess)))} guesses.")
                    if self.endDialog():
                        self.reset()
                    else:
                        loopFlag = False
                else:
                    self.guessCount += 1
            elif userInput.lower()[0] == "r":
                print(self.wordToGuess)
            elif userInput.lower()[0] == "b":
                pass
            elif userInput.lower()[0] == "e":
                loopFlag = False

if __name__ == "__main__":
    # TODO migrate to separate file at a later date.
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