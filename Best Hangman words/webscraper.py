import requests
from bs4 import BeautifulSoup as bs
import time, random


def isvalid(word):
    #added sleep interval to prevent spam pinging the server
    time.sleep(random.randint(100, 1000)/1000)
    r = requests.get(f"https://www.dictionary.com/browse/{word}")
    print(r)

    # if page does not exist, return invalid word
    if r.status_code != 200:
        return 1
    else:
        soup = bs(r.content, 'html.parser')

        # Get all h2 tags and their text on webpage
        h2_tags = soup.find_all('h2')
        h2_texts = [tag.get_text(strip=True).lower() for tag in h2_tags]

        #phrases that will return an "invalid word"
        invalid_cues = [
            "abbreviation for",
            "symbol for",
            "initialism for",
            "acronym for",
            "short for",
            "trademark"
        ]

        # Check if any h2 contains any of those phrases
        if any(any(cue in text for cue in invalid_cues) for text in h2_texts):
            return 1
        else:
            return 0