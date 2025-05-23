import requests
from bs4 import BeautifulSoup as bs
r = requests.get("https://www.dictionary.com/browse/thru")
print(r)
 
if r.status_code == 404:
    print("invalid word")
else:
    soup = bs(r.content, 'html.parser')

    # Get all h2 tags and their text
    content = soup.find_all('h2')
    texts = [tag.get_text(strip=True).lower() for tag in content]

    # Count how many h2 tags contain "abbreviation for"
    count = sum(1 for text in texts if "abbreviation for" in text)

    if count > 0:
        print("invalid word")
    else:
        print("valid word")
