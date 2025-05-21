import re


class WordSpecies:
    def __init__(self, wordData, vowelType):
        self.wordData = [word[1] for word in wordData]
        self.wordList = [word[0] for word in wordData]
        self.adjustedWordScore = []
        self.vowelType = vowelType  
         
    def applyConsonantRatio(self):
        self.adjustedWordScore = []
        for index, word in enumerate(self.wordList):
            consonant_count = len(re.sub(f'[{self.vowelType}]+', '', word, flags=re.DOTALL))
            consonant_ratio = round(consonant_count / len(word), 3)
            self.adjustedWordScore.append((word, round(consonant_ratio * self.wordData[index], 3)))
        
        return self.adjustedWordScore

    def __str__(self):
        return '\n'.join(self.adjustedWordScore)
    

if __name__ == '__main__': # test example
    pass
