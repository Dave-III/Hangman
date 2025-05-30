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
        self.wordLength = 0
        self.guessCount = 0
        self.guessedLetters = []

        with open(utils.WORDLIST_PATH) as wordFile:
            self.wordlist = wordFile.read().splitlines()

        self.WORD_MAX = max([len(word) for word in self.wordlist])

    def selectWord(self):
        if self.wordLength == 0:
            self.wordToGuess = random.choice(self.wordlist)
        else:
            self.wordToGuess = random.choice([word for word in self.wordlist if len(word) == self.wordLength])
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

    def selectDialog(self):
        while True:
            try:
                userIn = input("How many letters? (leave blank for random):\n>>> ")
                if (input == ''):
                    self.wordLength = 0
                    break
                self.wordLength = int(userIn)
                if self.wordLength > self.WORD_MAX or self.wordLength <= 0:
                    print(f"Error: no words found with length {self.wordLength}")
                    continue
                break
            except ValueError:
                # TODO error check case high numbers for no words - e.g. 500 letter word
                print("Error: must be a number")

    def endDialog(self):
        userIn = utils.askUntilValid("[New Word] [Exit]\n>>> ", EXIT_VALID + ["nw", "n", "new word", "new", "word"])
        if userIn in EXIT_VALID:
            return False
        else:
            utils.TerminalColours.printColour(utils.TerminalColours.BLD_CYAN, "---------- NEW GAME ----------")
            return True

    def main(self):
        self.selectDialog()
        self.reset()
        loopFlag = True
        while loopFlag:
            print(f"Current Word State ({len(self.wordState)} letters): {self.wordState}")
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
                self.wordState = ''.join([
                    userLetter.lower() if self.wordToGuess[index] == userLetter
                    else self.wordState[index]
                    for index in range(len(self.wordToGuess))
                ])
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