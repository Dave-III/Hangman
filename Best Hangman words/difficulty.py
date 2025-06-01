from consecutiveConsonants import WordSpecies
from collections import defaultdict

class LetterValue:

    def __init__(self, filename):
        #Alphabet dictionary used for collecting total count of each letter.
        self.alp_list = {
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0,
            "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0,
            "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0
        }
        with open(filename, "r") as file:
            self.file_data = file.read().splitlines()

    #Function used to claculate amount of each letter.
    def alp_list_calculator(self):
        for word in self.file_data:
            for letter in word.lower():
                if letter in self.alp_list:
                    self.alp_list[letter] += 1

class WordScore:

    #Initializes All items used for calculating each words score.
    def __init__(self):
        self.data = LetterValue("words_alpha.txt") #File that contains all the words
        self.data.alp_list_calculator() #num of letter data
        self.letter_scores = {ch: 1 / freq for ch, freq in self.data.alp_list.items() if freq > 0} # inverse of letter amount, helps with score
        self.score =[] #score of each letter, stored in this list
        self.top_scorers = [] # list of top scorers, depends on what the value of top scorers is set to
        self.penalty_letters = set('tnshrdlaeiou') #list that penalizes total score if these letters are in it W.I.P
        self.blacklist = "" #temp str, used for blacklisted letters requested from user.


    def score_word(self, word_length=1): #penalty factor is penalty due to using penalty letter W.I.P
        
        penalty_factor = 0.5
        for word in self.data.file_data:

            # If any letter from blacklist in word then the word is skipped
            if any(letter in self.blacklist for letter in word):
                continue

            # base score calculated from sum of letter score
            base_score = sum(self.letter_scores.get(ch, 0) for ch in word)

            # If any letter from word is in penalty letters, word is timesed by penalty factor W.I.P
            if any(letter in self.penalty_letters for letter in word):
                score = base_score * (1 - penalty_factor)
            else:
                score = base_score
 
            # multiplies score by 100000 to ensure human readability
            score = round(score * 100000, 3)
            if len(word) != word_length:
                continue
            else:
                # score of the word is added to score list as tuple.
                self.score.append((word, score))


    # setup for blacklist, turns letters given by user into traversable list
    def blacklist_sort(self):
        self.blacklist = list(self.blacklist)
        
    # function returns hardest word according to calculator for hangman
    def get_rarest(self):

        # collects edited score form Calvins consecutiveConsonants.py code
        correct_len_list = WordSpecies(self.score, "aeiouy")
        correct_len_list = correct_len_list.applyConsonantRatio()

        #returns second item from score tuple
        def get_score(item):
            return item[1]
        
        #sorts the words of correct length in terms of the score in reverse so max score is first
        correct_len_list.sort(key=get_score, reverse=True)

        #returns all words with correct length in sorted order from highest score to lowest
        self.top_scorers = correct_len_list
        return self.top_scorers

    def wordpicker(self, user_dif=2):
        top_scores = self.get_rarest()
        import random
        
        
        total = len(top_scores)
        if user_dif == 1:
            lowest = total * 2 // 3
            highest = total - 1
        
        if user_dif == 2:
            lowest = total//3
            highest = total * 2 // 3 - 1
        
        if user_dif == 3:
            lowest = 0
            highest = total//3 - 1

        rank = random.randint(lowest, highest)
        return top_scores[rank]
        
    #adds UI for the code, allows user to see result
    def __str__(self):
        print('\n')

        
        user_input = int(input("What length of word do you want: "))

        self.blacklist = input("Are there any letters you do want to remove (if multiple letters, type them with no spacing): ")

        print("\n")
        
        self.score_word(user_input) #collects all word scores
        top_scorers = self.get_rarest() #collects highest scoring words based off user input.

        
        if self.top_scorers == []: #if the list is empty prompts user with error (fail-safe)
            return f"There are no words in the English dictionary with a length of {user_input} letters."
        
        #calculates average score of all words under user restriction
        total = 0
        for i in self.top_scorers:
            total += i[1]
        average = round(total / len(self.top_scorers), 3)

        #finds closest word to average calculated above
        closest_word = min(self.top_scorers,key=lambda x: abs(x[1] - average))


        count = 1 #count used for nice formatting
        top_ten = self.top_scorers[:10]
        for i in top_ten: #prints top ten, interchangeable by coder
            print(f"No. {count} = {i[0]} with a score of {i[1]}")
            count += 1

        print("\n")
        print(f"Total number of words with a size of {user_input} is {len(self.top_scorers)}, and the average score was {average}")

        random_word = self.wordpicker(user_input)
        print()
        print(f"random word picked under user difficulty is {random_word[0]} with a score of {random_word[1]}")
        print()

        return f"The closest word to the average is '{closest_word[0]}' with a score of {closest_word[1]}"

class WordScoring: # higher score -> harder
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.scores = {}
        self.letterCount = defaultdict(0)
        for word in wordlist:
            for letter in list(word):
                self.letterCount[letter] += 1
        self.letterWeight = {ch: 1 / freq for ch, freq in self.letterCount.items() if freq > 0} 

        self.applyLetterWeight()
        self.applyLengthBias()

    def __iter__(self):
        pass

    def applyLengthBias(self):
        def lengthEqu(wordLength):
            # shortest word - 2 unique letters(?)
            # most unique - 16 unique letters, always guessable w/ 10 lives
            return (-14 * wordLength**2) + 16
        
        for word in self.wordlist:
            self.scores[word] *= lengthEqu(len(word))
        

    # probably ideal to wrap in loading text
    def applyLetterWeight(self):
        for word in self.wordlist:
            # split word into set (remove duplicates), and sum weights
            score = sum([self.letterWeight.get(letter) for letter in set(list(word))])
            self.scores[word] = score


if __name__ == "__main__":
    #calls the function
    ws = WordScore()
    print(ws)