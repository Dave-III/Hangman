import requests
from bs4 import BeautifulSoup as bs
r = requests.get("https://www.dictionary.com/browse/thru")
print(r)
soup = bs(r.content, 'html.parser')
 
s = soup.find('div', class_='NZKOFkdkcvYgD3lqOIJw')
content = soup.find_all('h2')
texts = [tag.get_text(strip=True) for tag in content]
count = 0

print()
print(s)
print()
if ""

for h2 in content:

    if "abbreviation for" in h2:
        count += 1

if count > 0:
    print("invalid word")
else:
    print(content)
