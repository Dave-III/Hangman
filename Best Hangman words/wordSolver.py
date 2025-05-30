from utils import WORDLIST_PATH
from collections import defaultdict

NULL_CHARS = ['-', '_', '*', '/']
BLACKLIST_STR = r"!@#$%^&*()_-+=[]\\|;':<,>.?/"
TERMINAL_LINE_LIMIT = 120

# TODO add letter progress indicator
# TODO have initial word length query

class HangmanSolver:
    def __init__(self, wordLength: int, verbose = False):
        self.length = wordLength
        self.verbose = verbose
        self.initialiseWordList()

    def initialiseWordList(self):
        with open(WORDLIST_PATH, "r") as file:
            self.wordList = [word for word in file.read().splitlines() if len(word) == self.length]
        if self.verbose:
            print(f"Word List initialised: {len(self.wordList)} words.")

    def addLetters(self, wordState: str) -> None:
        """Filters wordlist by letters at specific placements.

        :param wordState: the partially constructed word, with NULL_CHARS as unknowns
        :type wordState: str
        """

        # denote which indices are known - not null
        indexToChar = {}
        for index, char in enumerate(list(wordState)):
            if all(i not in char for i in NULL_CHARS):
                indexToChar[index]=char
    
        wordsToRemove = []
        # iterate over word list to append to new effective list
        for word in self.wordList:
            for key, value in indexToChar.items(): # iterates over all known letter locations
                # condition 1 - character at same index doesn't match
                # condition 2 - number of character instances aren't the same
                if word[key] != value or word.count(value) != list(indexToChar.values()).count(value):
                    wordsToRemove.append(word)
        
        # filters violating words
        for word in wordsToRemove:
            self.wordList.remove(word)
        if self.verbose:
            self.printCandidates()

    def removeLetters(self, lettersToRemove: str) -> None:
        """Filters wordlist by absence of letters within strings.

        :param lettersToRemove: a string containing letter/s disallowed within each word
        :type lettersToRemove: str
        """
        # removes words if containing any characters defined as disallowed
        self.wordList = [word for word in self.wordList if not any(letter in word for letter in list(lettersToRemove))]
        if self.verbose:
            self.printCandidates()

    def suggestWords(self) -> list: #TODO change for individual letter weights instead of purely the most common
        """Given a wordlist, select the most probable based on letter probability. Uses self.wordList for word set.
        """
        # creates a dictionary for each character in a word
        # countdict = [{} for _ in range(self.length)]
        countdict = [defaultdict(int)] * self.length

        # iterates over each character in each word
        for word in self.wordList:
            for index, char in enumerate(word):
                countdict[index][char] += 1

        # join letters associated with highest frequency for each dict
        commonLetterString = ''.join([max(dictindex,key=dictindex.get) for dictindex in countdict])

        # create padded list
        similarityList = [0] * len(self.wordList)

        # loop determines the number of matched characters from each word to common_letter_string
        for wordId, word in enumerate(self.wordList):
            # iterate over each letter in word, increment if values match
            for index in range(0,len(word)):
                if word[index] == commonLetterString[index]:
                    similarityList[wordId] += 1 # increment value

        max_match = max(similarityList)
        # get all words that match the most characters to common_letter_string
        matchedwords = [self.wordList[index] for index,match_count in enumerate(similarityList) if match_count == max_match]
        print("The following words are likely to result in a win or further info:")
        return matchedwords

    def printCandidates(self, wordList: list = None, rowMaxWords:int = 10) -> None:
        """Arranges and prints list elements into rows of variable length.

        :param wordList: The list of words to print. Defaults to None, causes self.wordList
        :type wordList: list[str] 

        :param rowMaxWords: maximum number of elements per row, defaults to 10
        :type rowMaxWords: int
        """
        # default catch - use current word list
        if wordList == None:
            wordList = self.wordList

        words_per_row = min(rowMaxWords,TERMINAL_LINE_LIMIT//(self.length+3))
        wholestring = ''
        for index, word in enumerate(wordList, start=1):
            # break row at max number
            if index % words_per_row == 0:
                wholestring += f"{word}\n" 
            # add spacing between elements
            else:
                wholestring += f"{word}   "

        print(wholestring)

    def evaluateState(self) -> None:
        if len(self.wordList) == 1:
            print(f"\nThe only available word is:\n\t{self.wordList[0]}\nProgram is Exiting...")
        elif len(self.wordList) == 0:
            print("\nThere are no words available. Restarting wordlist...\n")

    def start(self) -> None:
        """User-wrapper to evaluate hangman word through user-input via CLI.
        """
        exitState = False # controls whether exit state
        while not exitState: # while exit not called
            try:
                user_state = int(input(f"{len(self.wordList)} words are possible.\n[1] Add discovered letter\n[2] Remove absent letter\n[3] Suggest Word\n[4] Show Possible Words\n[5] Exit\n>>> "))
            except ValueError: # if not number, make arbitrary number for default case to catch
                user_state = -1

            # evaluate condition based on user_state value
            match user_state:
                case 1: # discovered letter
                    wordstate = input("Current Word State:\n>>> ")
                    self.addLetters(wordstate.lower())
                case 2: # absent letter
                    wordstate = input("Absent Letter(s):\n>>> ")
                    self.removeLetters(wordstate.lower())
                case 3: # suggest words based on probability
                    print("The following words are most likely correct:")
                    self.printCandidates(self.suggestWords())
                case 4: # view possible words
                    self.printCandidates()
                case 5: # exits CLI
                    exitState = True
                    break
                case _: # unexpected input
                    print("Invalid Input. Please Try Again.")

            self.evaluateState()

if __name__ == "__main__":
    q = HangmanSolver(10, True)
    q.start()