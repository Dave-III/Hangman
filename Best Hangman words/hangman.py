import random
import utils
from utils import TerminalColours as tc
import wordSolver

# TODO by chance, words can be randomly selected consecutively

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
            print(f"\t{tc.applyColour((tc.REG_GREEN if letter in self.wordToGuess else tc.REG_RED), letter)}", end='')
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
                if (userIn == ''):
                    self.wordLength = 0
                    break
                self.wordLength = int(userIn)
                if self.wordLength > self.WORD_MAX or self.wordLength <= 0:
                    print(f"Error: no words found with length {self.wordLength}")
                    continue
                break
            except ValueError:
                print("Error: must be a number")

    def endDialog(self):
        userIn = utils.askUntilValid("[New Word] [Exit]\n>>> ", ["exit", "e"] + ["nw", "n", "new word", "new", "word"])
        if userIn in ["exit", "e"]:
            return False
        else:
            tc.printColour(tc.BLD_CYAN, "---------- NEW GAME ----------")
            return True

    def main(self):
        self.selectDialog()
        self.reset()
        while True:
            print(f"Current Word State ({len(self.wordState)} letters): {self.wordState}")
            if self.guessCount != 0:
                self.showGuessed()
            userInput = input("\nType any letter, or:\n[Restart] [Back] [Exit]\n>>> ").lower()
            if userInput == "restart":
                tc.printColour(tc.BLD_CYAN, "\nRestarting...")
                self.reset()
            elif userInput == "back":
                tc.printColour(tc.BLD_CYAN, "\nExiting Hangman Game...")
                return 1
            elif userInput == "exit":
                tc.printColour(tc.BLD_CYAN, "\nExiting Program...")
                return 0
            else:
                if len(userInput) != 1: # longer than 1 letter
                    tc.printColour(tc.REG_RED, "Error: Must input a single letter!\n")
                    continue
                elif userInput not in list("abcdefghijklmnopqrstuvwyxz"): # not alphabetical
                    tc.printColour(tc.REG_RED, "Error: Must not be a number or special character!\n")
                    continue
                elif userInput in self.guessedLetters: # already guessed
                    tc.printColour(tc.REG_RED, "Error: Letter has already been guessed!\n")
                    continue
                else:
                    self.wordState = ''.join([
                        userInput if self.wordToGuess[index] == userInput
                        else self.wordState[index]
                        for index in range(len(self.wordToGuess))
                    ])
                    self.guessedLetters.append(userInput)
                    if self.wordState == self.wordToGuess:
                        print(f"You have guessed the word {tc.applyColour(tc.BLD_YELLOW, self.wordToGuess)} in {tc.applyColour(tc.REG_YELLOW, self.guessCount)} guesses!\n" +
                              f"Optimally, you could have guessed the word in {len(set(list(self.wordToGuess)))} guesses.")
                        if self.endDialog():
                            self.reset()
                        else:
                            tc.printColour(tc.BLD_CYAN, "\nExiting Program...")
                            return 0
                    else:
                        self.guessCount += 1

if __name__ == "__main__":
    print("Please run main.py...")