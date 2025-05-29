import random

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
            userInput = input("Select:\n[Guess Letter] [Restart] [Back] [Exit]\n>>> ")
            if userInput.lower() == "g":
                pass
            elif userInput.lower() == "r":
                print(self.wordToGuess)
            elif userInput.lower() == "b":
                pass
            elif userInput.lower() == "e":
                loopFlag = False

if __name__ == "__main__":
    q = HangmanSession()
    q.main()