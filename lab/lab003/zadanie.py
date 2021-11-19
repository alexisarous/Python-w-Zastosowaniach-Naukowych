from rich.console import Console
import rich.traceback
import requests
from bs4 import BeautifulSoup
import json
# import gzip
import argparse

console = Console()
console.clear()
rich.traceback.install()


parser = argparse.ArgumentParser(description="Opis")
parser.add_argument('file', help='name of file')
args = parser.parse_args()


req = requests.get('https://www.nature.com/nnano/')

# console.print(req.status_code)



soup = BeautifulSoup(req.text, 'html.parser')

divs_cat = soup.find('ul', class_ = 'app-article-list-row')
divs_arts = divs_cat.find_all('div', class_ = 'c-card__layout u-full-height')

x = []

for div in divs_arts:
    #console.print(f"{div.find('a').text.strip() = }")  
    #console.print(json.dumps(f"{div.find('a').text.strip()}"))
    x.append(json.dumps(f"{div.find('a').text.strip()}"))


title = args.file + ".json"

with open(title, 'w') as f:
    json.dump(x, f)


with open(title, 'r') as f:
    y = json.load(f)
    console.print(y)
