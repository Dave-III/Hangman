from collections import Counter

class LetterValue:

    def __init__(self, filename):
        self.alp_list = {
            "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0,
            "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0,
            "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0
        }
        with open(filename, "r") as file:
            self.file_data = file.read().splitlines()

    def alp_list_calculator(self):
        for word in self.file_data:
            for letter in word.lower():
                if letter in self.alp_list:
                    self.alp_list[letter] += 1

class WordScore:

    def __init__(self):
        self.data = LetterValue("words_alpha.txt")
        self.data.alp_list_calculator()
        self.letter_scores = {ch: 1 / freq for ch, freq in self.data.alp_list.items() if freq > 0}
        self.score =[]
        self.top_scorers = []
        self.penalty_letters = set('tnshrdlaeiou')
        self.blacklist = ""

    def score_word(self, repetition_factor=0.1, penalty_factor = 0.5):
        for word in self.data.file_data:
            
            if any(letter in self.blacklist for letter in word):
                    continue
            base_score = sum(self.letter_scores.get(ch, 0) for ch in word)

            counts = Counter(word)
            repeats = sum(count for count in counts.values() if count == 1)

            repetition_multiplier = 1 + (repeats * repetition_factor)
            score = base_score * repetition_multiplier

            score -= score * penalty_factor

            score = round(score * 100000, 3)

            self.score.append((word, score))

    def blacklist_sort(self):
        self.blacklist = list(self.blacklist)
        
    def get_rarest(self, length=1):
        correct_len_list = []
        for word, score in self.score:
            if len(word) == length:
                correct_len_list.append((word, score))

        def get_score(item):
            return item[1]
        
        correct_len_list.sort(key=get_score, reverse=True)

        self.top_scorers = correct_len_list

    def __str__(self):
        print('\n')

        
        user_input = int(input("What length of word do you want: "))
        self.blacklist = input("Are there any letters you do want in there (if multiple letters, type them with no spacing): ")
        print("\n")
        self.score_word()
        self.get_rarest(user_input)
        if self.top_scorers == []:
            return f"There are no words in the English dictionary with a length of {user_input} letters."
        total = 0
        for i in self.top_scorers:
            total += i[1]
        average = round(total / len(self.top_scorers), 3)

        closest_word = min(
        self.top_scorers,
        key=lambda x: abs(x[1] - average)
        )

        count = 1
        top_ten = self.top_scorers[:10]
        for i in top_ten:
            print(f"No. {count} = {i[0]} with a score of {i[1]}")
            count += 1
        print("\n")
        print(f"Total number of words with a size of {user_input} is {len(self.top_scorers)}, and the average score was {average}")

        return f"The closest word to the average is '{closest_word[0]}' with a score of {closest_word[1]}"

ws = WordScore()
print(ws)