import re

FILE_PATH = "words_alpha.txt"
HARD_VOWELS = ['a', 'e', 'i', 'o', 'u']
HARD_VOWELS_S = 'aeiou'
SOFT_VOWELS_S = 'aeiouy'

class wordSpecies:
    def __init__(self, wordlength, vowelType):
        self.vowelType = vowelType
        file = open(FILE_PATH, 'r')
        self.wordlist = [x for x in file.read().splitlines() if len(x) == wordlength]
        file.close()

    def get_consecutive(self, wordnum):
        maxCon = 0
        maxConList = []
        for x in self.wordlist:
            splitWord = re.split(f'[{self.vowelType}]+', x, flags=re.IGNORECASE)
            maxWordCon = max([len(y) for y in splitWord])
            if maxWordCon > maxCon:
                maxCon = maxWordCon
                maxConList = [x]
            elif maxWordCon == maxCon:
                maxConList.append(x)
        return (maxCon, maxConList[:wordnum-1]) # return wordnum number of words


    def __str__(self):
        return '\n'.join(self.wordlist)
    

if __name__ == '__main__': # test example
    q = input("word length:\n>>> ")
    w = wordSpecies(int(q), SOFT_VOWELS_S)
    print(w.get_consecutive(10))
