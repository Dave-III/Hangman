import requests
from bs4 import BeautifulSoup as bs
import time, random
from utils import BufferText #imported for customised displays.
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# -------------------- Validate_Word_Wrapper Function --------------------
# This wrapper function allows class methods inside Pool.map for both Windows and MacOS.
# It receives a (validator_instance, word) tuple and returns the validation result.
def validate_word_wrapper(args):
    validator, word = args
    return validator.isvalid(word)

#--------------------- WordValidator Class --------------------
#Class used to ping dictionary.com and wiktionary.com with words from words_alpha.txt
#If no response returns false and removes word from words_alpha.txt.
# and filters out abbreviations, trademarks, etc.

class WordValidator:

    def __init__(self, num_workers=0):

        # Limit number of worker processes to avoid overwhelming the system or target sites
        self.num_workers = min(32, cpu_count()) if num_workers is None else num_workers

        #phrases in definition that suggest that word is not a standard dictionary word.
        #customised for dicctionary.com
        self.dict_invalid_cues = [
                "abbreviation for","symbol for","initialism for",
                "acronym for","short for","trademark"
                ]
        
        #phrases in definition of word that suggest that it is not a standard dictionary word.
        #customised for wiktionary.com

        #ISSUE: wiktionary contains many definitions as an example "a" is a real word but also an acronym for
        #lots of other words therefore it gets taken off the list.
        self.wikt_invalid_cues = [
            "acronym of", "abbreviation of", "initialism of", "short for",
            "trademark of", "symbol for", "contraction of", "pronunciation spelling of",
            "eye dialect of", "nonstandard spelling of", "obsolete spelling of",
            "rare spelling of", "misspelling of", "dated spelling of"
            ]

# -------------------- isvalid --------------------
# Determines if a word is valid based on its dictionary.com or wiktionary entry
# Returns (word, True/False)
    def isvalid(self, word):
        #added sleep interval to prevent spam pinging the server
        time.sleep(random.randint(100, 250)/1000)

        try:
            #First attempt: dictionary.com
            
            web_dict = requests.get(f"https://www.dictionary.com/browse/{word}", timeout=5)

            #if dictionary.com doesn't have word, try Wiktionary
            if web_dict.status_code != 200:
                
                web_wikt = requests.get(f"https://en.wiktionary.org/wiki/{word}", timeout=5)

                #if Wiktionary doesn't work, word is invalid and return False
                if web_wikt.status_code != 200:
                    return (word, False)

                #if word exists scan Wiktionary entry for phrases suggesting non-standard word
                broth = bs(web_wikt.content, 'html.parser')
                main_tag = broth.find("div", {"class": "mw-content-ltr"})

                #if no definition, word is invalid and return False
                if not main_tag:
                    return (word, False)


                main_text = main_tag.get_text().splitlines()
                for line in main_text:
                    #if any phrase in word def is in wikt_invalid_cues, word is invalid and return False
                    if any(cue in line for cue in self.wikt_invalid_cues):
                        return (word, False)
                #else return True
                return (word, True)

            else:
                #if word exists on dictionary.com scan page for definition under 'h2' tag
                soup = bs(web_dict.content, 'html.parser')
                h2_tags = soup.find_all('h2')
                h2_texts = [tag.get_text(strip=True).lower() for tag in h2_tags]

                #if any phrase in 'h2' tag in dict_invalid_cues, word is invalid and return False
                if any(any(cue in text for cue in self.dict_invalid_cues) for text in h2_texts):
                    return (word, False)
                
                #else return True
                else:
                    return (word, True)
                
        #exception case to prevent errors.
        except Exception as e:
            print(f"Error on word '{word}': {e}")

            #default returns False
            return (word, False)

# -------------------- validate_words --------------------
# Uses multiprocessing to validate a list of words in parallel
# Returns a dictionary of {word: True/False}

    def validate_words(self, words):
        results = {}
        with Pool(processes=self.num_workers) as pool:
            # Use imap_unordered to get results as they come in, and wrap in tqdm for progress bar
            
            for word_result in tqdm(
                pool.imap_unordered(validate_word_wrapper, [(self, word) for word in words]),
                total=len(words),desc=f"Validating words",dynamic_ncols=True):

                word, is_valid = word_result
                results[word] = is_valid

                with BufferText.loadingText(f"Validated: {word}"):
                    pass
        return results
    
# -------------------- __name__ == '__main__' --------------------
# Protects multiprocessing code from being executed on import
if __name__ == "__main__":

    #example words
    words_to_check = ["aardvarks", "NASA", "xyzabc", "example", "OMG"]

    #validator running 12 processes at the same time
    validator = WordValidator(num_workers=12)

    #process words in parallel
    result = validator.validate_words(words_to_check)

    #print results
    for word, valid in result.items():
        print(f"{word}: {'Valid' if valid else 'Invalid'}")