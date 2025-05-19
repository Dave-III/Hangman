import re

FILE_PATH = "words_alpha.txt"
HARD_VOWELS = ['a', 'e', 'i', 'o', 'u']
HARD_VOWELS_S = 'aeiou'
SOFT_VOWELS_S = 'aeiouy'

class wordSpecies:
    def __init__(self, wordlength, vowelType):
        # determines vowels to check (generally, 'y' inclusive or not)
        self.vowelType = vowelType

        # grab all words of defined length, after trimming whitespace
        with open(FILE_PATH, 'r') as file:
            self.wordlist = [x.strip() for x in file.read().splitlines() if len(x.strip()) == wordlength]

    def get_consecutive(self, wordnum = None, trimDoubleLetter = False):
        maxCon = 0
        maxConList = []
        for x in self.wordlist:

            # if enabled, removes all consecutive instances of letters (e.g. converts "bully" into "buly")
            if trimDoubleLetter:
                x = re.sub(f'([^{self.vowelType}])(?=(?:\\1))', '', x, flags=re.DOTALL)

            # find largest consonant streak
            splitWord = re.split(f'[{self.vowelType}]+', x, flags=re.IGNORECASE)
            maxWordCon = max([len(y) for y in splitWord])

            # if longer consonant streak found, wipe list and add word
            if maxWordCon > maxCon:
                maxCon = maxWordCon
                maxConList = [x]
            # if equal consonant streak found, add to list
            elif maxWordCon == maxCon:
                maxConList.append(x)

        return (maxCon, maxConList[:wordnum]) # return wordnum number of words


    def __str__(self):
        # prints all words of initialised length
        return '\n'.join(self.wordlist)
    

if __name__ == '__main__': # test example
    q = input("word length:\n>>> ")
    w = wordSpecies(int(q), HARD_VOWELS_S)
    print(w.get_consecutive(trimDoubleLetter=True))
