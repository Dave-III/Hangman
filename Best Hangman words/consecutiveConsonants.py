import re
import math
import statistics

class WordSpecies:
    def __init__(self, wordData, vowelType):
        self.wordScore = [word[1] for word in wordData]
        self.wordList = [word[0] for word in wordData]
        self.adjustedWordScore = []
        self.vowelType = vowelType  
         
    def applyConsonantRatio(self):
        ratios = []
        for word in self.wordList:
            consonant_count = len(re.sub(f'[{self.vowelType}]+', '', word, flags=re.DOTALL))
            ratios.append(consonant_count / len(word))

        self.mean = round(sum(ratios)/len(ratios), 3)
        self.std = statistics.stdev(ratios)

        for index, ratio in enumerate(ratios):
            self.adjustedWordScore.append((self.wordList[index], round(self.inverseWeightEquation(ratio) * self.wordScore[index], 3)))
        
        return self.adjustedWordScore
    
    # def inverseWeightEquation(self, score):
    #     return (1/1.425)*(1-math.exp(-(score-0.6)**2/(0.25**2))) + 0.5
    
    def inverseWeightEquation(self, score):
        return (1/1.425)*(1-math.exp(-(score-self.mean)**2/(8*(self.std**2)))) + 0.5
    
    def summaryStats(self):
        newScore = [word[1] for word in self.adjustedWordScore]
        print(f"mean: {round(sum(newScore)/len(newScore), 3)}")
        print(f"std: {statistics.stdev(newScore)}")


    def __str__(self):
        return '\n'.join(self.adjustedWordScore)
    

if __name__ == '__main__': # test example
    with open("words_alpha.txt", "r") as file:
        wordlist = [word for word in file.read().splitlines()]
    wordBaseScore = [(word, 1) for word in wordlist]
    q = WordSpecies(wordBaseScore, "aeiou")
    q.applyConsonantRatio()
    q.summaryStats()
    pass
