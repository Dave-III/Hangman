"""The main hangman game script, wrapped into a `HangmanSession` class.

To use, create a `HangmanSession` and call `main()`.
"""

import random
import utils
from utils import TerminalColours as tc

# TODO by chance, words can be randomly selected consecutively

class HangmanSession:

    def __init__(self):
        """Initialises base variables for later use, and reads a file for all words to select from (currently static location)."""
        self.wordToGuess = ''
        self.wordState = None
        self.wordLength = 0
        self.guessCount = 0
        self.guessedLetters = []

        with open(utils.WORDLIST_PATH) as wordFile:
            self.wordlist = wordFile.read().splitlines()

        self.WORD_MAX = max([len(word) for word in self.wordlist])

    def __selectWord(self):
        """Selects the word to be used, considering the user-input for word length"""
        if self.wordLength == 0:
            self.wordToGuess = random.choice(self.wordlist)
        else:
            self.wordToGuess = random.choice([word for word in self.wordlist if len(word) == self.wordLength])
        self.wordState = "_" * len(self.wordToGuess)

    def __showGuessed(self):
        """Helper function to show all guessed letters to a width of 5, with colouring depending on inclusion/exclusion."""
        print("Guessed Letters:")
        for counter, letter in enumerate(self.guessedLetters, start = 1):
            print(f"\t{tc.applyColour((tc.REG_GREEN if letter in self.wordToGuess else tc.REG_RED), letter)}", end='')
            if (counter % 5 == 0):
                print()
        print()
      
    def __reset(self):
        """Helper function to reset the game, reverting guessed letters and selecting a new word."""
        self.guessCount = 0
        self.guessedLetters = []
        self.__selectWord()

    def __selectDialog(self):
        """Helper function to query the user (with rough sanitation) for word length to guess."""
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

    def __endDialog(self):
        """Helper function to query the user what to do once the game has ended.
        
        :returns: A boolean `True` starts a new game, while `False` exits the program."""
        userIn = utils.askUntilValid("[New Word] [Exit]\n>>> ", ["exit", "e"] + ["nw", "n", "new word", "new", "word"])
        if userIn in ["exit", "e"]:
            return False
        else:
            tc.printColour(tc.BLD_CYAN, "---------- NEW GAME ----------")
            return True

    def main(self):
        """The main run function of the Hangman game.
        
        :returns:
            An integer indicating intent to the main handler.\n
            - 0 = exit the program\n
            - 1 = continue the outer loop"""
        self.__selectDialog()
        self.__reset()
        while True:
            # Base Information printing
            print(f"Current Word State ({len(self.wordState)} letters): {self.wordState}")
            if self.guessCount != 0:
                self.__showGuessed()

            # Queries user input for special function or letter guessing
            userInput = input("\nType any letter, or:\n[Restart] [Back] [Exit]\n>>> ").lower()
            if userInput == "restart":
                tc.printColour(tc.BLD_CYAN, "\nRestarting...")
                self.__reset()
            elif userInput == "back":
                tc.printColour(tc.BLD_CYAN, "\nExiting Hangman Game...")
                return 1
            elif userInput == "exit":
                tc.printColour(tc.BLD_CYAN, "\nExiting Program...")
                return 0
            
            # if letter guessing,
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

                # if valid, add letter, else keep previous letter
                else:
                    self.wordState = ''.join([
                        new if new == userInput else old
                        for new, old in zip(self.wordToGuess, self.wordState)
                    ])
                    self.guessedLetters.append(userInput)

                    # if word has been fully guessed
                    if self.wordState == self.wordToGuess:
                        print(f"You have guessed the word {tc.applyColour(tc.BLD_YELLOW, self.wordToGuess)} in {tc.applyColour(tc.REG_YELLOW, self.guessCount)} guesses!\n" +
                              f"Optimally, you could have guessed the word in {len(set(list(self.wordToGuess)))} guesses.")
                        if self.__endDialog():
                            self.__reset()
                        else:
                            tc.printColour(tc.BLD_CYAN, "\nExiting Program...")
                            return 0
                    else:
                        self.guessCount += 1

if __name__ == "__main__":
    print("Please run main.py...")