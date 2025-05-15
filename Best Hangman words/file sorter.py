
def file_sorter(filename):
    with open(filename, "r+") as file:
        file_data = file.read().splitlines()
        blacklist_words = []
        for word in file_data:
            word = word.lower()
            word_list = list(word)
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

        print(blacklist_words)

filename = input("enter filename: ")
file_sorter(filename)