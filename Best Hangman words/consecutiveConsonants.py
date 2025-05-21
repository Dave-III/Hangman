import re

FILE_PATH = "words_alpha.txt"
HARD_VOWELS = ['a', 'e', 'i', 'o', 'u']
HARD_VOWELS_S = 'aeiou'
SOFT_VOWELS_S = 'aeiouy'

# class wordSpecies:
#     def __init__(self, wordlength, vowelType):
#         # determines vowels to check (generally, 'y' inclusive or not)
#         self.vowelType = vowelType

#         # grab all words of defined length, after trimming whitespace
#         with open(FILE_PATH, 'r') as file:
#             self.wordlist = [x.strip() for x in file.read().splitlines() if len(x.strip()) == wordlength]

#     def set_wordlength(self, length: int):
#         # grab all words of defined length, after trimming whitespace
#         with open(FILE_PATH, 'r') as file:
#             self.wordlist = [x.strip() for x in file.read().splitlines() if len(x.strip()) == length]

#     def get_longest_consecutive(self, wordnum = None, trimDoubleLetter = False):
#         maxCon = 0
#         maxConList = []
#         for x in self.wordlist:

#             # if enabled, removes all consecutive instances of letters (e.g. converts "bully" into "buly")
#             if trimDoubleLetter:
#                 x = re.sub(f'([^{self.vowelType}])(?=(?:\\1))', '', x, flags=re.DOTALL)

#             # find largest consonant streak
#             splitWord = re.split(f'[{self.vowelType}]+', x, flags=re.IGNORECASE)
#             maxWordCon = max([len(y) for y in splitWord])

#             # if longer consonant streak found, wipe list and add word
#             if maxWordCon > maxCon:
#                 maxCon = maxWordCon
#                 maxConList = [x]
#             # if equal consonant streak found, add to list
#             elif maxWordCon == maxCon:
#                 maxConList.append(x)

#         return (maxCon, maxConList[:wordnum]) # return wordnum number of words
    
#     def get_most_consonants(self, wordnum = None):
#         consonant_ratios = []
#         for word in self.wordlist:
#             original_length = len(word)
#             consonant_count = len(re.sub(f'[{self.vowelType}]+', '', word, flags=re.DOTALL))
#             consonant_ratios.append((word, round(consonant_count / original_length, 3)))
#         consonant_ratios.sort(key=lambda x: x[1], reverse=True)
#         return consonant_ratios[:wordnum]


#     def __str__(self):
#         # prints all words of initialised length
#         return '\n'.join(self.wordlist)
    

class WordSpecies:
    def __init__(self, wordData, wordLength, vowelType):
        self.wordData = [word.strip() for word in wordData if len(word.strip()) == wordLength]
        self.wordList = [word[0] for word in self.wordData]
        self.adjustedWordScore = []
    
    def applyConsonantRatio(self):
        self.adjustedWordScore = []
        for index, word in enumerate(self.wordList):
            consonant_count = len(re.sub(f'[{self.vowelType}]+', '', word, flags=re.DOTALL))
            consonant_ratio = round(consonant_count / len(word), 3)
            self.adjustedWordScore.append((word, round(consonant_ratio * self.wordData[index][1], 3)))
        
        return self.adjustedWordScore

    def __str__(self):
        return '\n'.join(self.adjustedWordScore)
    

if __name__ == '__main__': # test example
    q = input("word length:\n>>> ")
    # w = WordSpecies(int(q), SOFT_VOWELS_S)
    # # print(w.get_longest_consecutive(trimDoubleLetter=True))
    # print(w.)
