import requests
from bs4 import BeautifulSoup as bs
import time, random
from utils import BufferText


def isvalid(word):

    #phrases that will return an "invalid word"
    dict_invalid_cues = [
            "abbreviation for",
            "symbol for",
            "initialism for",
            "acronym for",
            "short for",
            "trademark"]
    wikt_invalid_cues = [
        "acronym of", "abbreviation of", "initialism of", "short for",
        "trademark of", "symbol for", "contraction of", "pronunciation spelling of",
        "eye dialect of", "nonstandard spelling of", "obsolete spelling of",
        "rare spelling of", "misspelling of", "dated spelling of"]
    

    #added sleep interval to prevent spam pinging the server
    time.sleep(random.randint(100, 1000)/1000)
    BufferText.start()
    web_dict = requests.get(f"https://www.dictionary.com/browse/{word}")
    BufferText.stop()
    print(web_dict)


    # if page does not exist, return invalid word
    if web_dict.status_code != 200:
        BufferText.start()
        web_wikt = requests.get(f"https://en.wiktionary.org/wiki/{word}")
        BufferText.stop()
        print(web_wikt)
        if web_wikt.status_code != 200:
            return False
        else:
            broth = bs(web_wikt.content, 'html.parser')
            main_tag = broth.find_all("div", {"class": "mw-content-ltr"})[0]
            main_text = main_tag.get_text()
            main_text = main_text.splitlines()
            for line in main_text:
                if any(cue in line for cue in wikt_invalid_cues):
                    return False
            return True
            
    else:
        soup = bs(web_dict.content, 'html.parser')

        # Get all h2 tags and their text on webpage
        h2_tags = soup.find_all('h2')
        h2_texts = [tag.get_text(strip=True).lower() for tag in h2_tags]

        # Check if any h2 contains any of those phrases
        if any(any(cue in text for cue in dict_invalid_cues) for text in h2_texts):
            return False
        else:
            return True

if __name__ == "__main__":
    isvalid("aardvarks")