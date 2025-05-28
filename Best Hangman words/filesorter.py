from webscraper import isvalid


""" Removes all words in a given file that does not contain any vowels (including y)"""

def file_sorter(filename):
    with open(filename, "r+") as file:
        file_data = file.read().splitlines()
        blacklist_words = []
        count = 0
        total = 0
        for word in file_data:
            #currently if it finds 100 invalid words it will break the loop
            if count == 20:
                break
            #if the word is invalid then prints the word
            total += 1
            if not isvalid(word):
                blacklist_words.append(word)
                count += 1
            word = word.lower()
            word_list = list(word)
            # untested alternative
            # if all(x not in word_list for x in ['a', 'e', 'i', 'o', 'u', 'y']):
            #     blacklist_words.append(word)
            if "a" not in word_list:
                if "e" not in word_list:
                    if "i" not in word_list:
                        if "o" not in word_list:
                            if "u" not in word_list:
                                if "y" not in word_list:
                                    blacklist_words.append(word)
        file.seek(0)
        
        for word in file_data:
            if word not in blacklist_words:
                file.write(word + "\n")

        file.truncate()

        for word in blacklist_words:
            print(word, end=" ")
        print(count)
        print(total)

filename = input("enter filename: ")
file_sorter(filename)