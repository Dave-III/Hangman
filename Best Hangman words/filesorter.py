from webscraper import WordValidator


""" Removes all words in a given file that does not contain any vowels (including y)"""

def file_sorter(filename, size):
    with open(filename, "r+") as file:
        blacklist_words = []
        file_data = file.read().splitlines()
        validator = WordValidator(num_workers=12)  # Create once
        results = validator.validate_words(file_data[:300])  # Pass full list at once

        blacklist_words = [word for word, valid in results.items() if not valid]
        return blacklist_words
        # Rewind file pointer and write only valid words back
        """file.seek(0)
        for word in file_data:
            if word not in blacklist_words:
                file.write(word + "\n")
        file.truncate()

        # Print blacklisted words for info
        for word in blacklist_words:
            print(word, end=" ")
        print(f"\nTotal blacklisted words: {len(blacklist_words)}")"""


if __name__ == "__main__":
    all_words = file_sorter("words_alpha.txt", 100)
    for word in all_words:
        print(word)