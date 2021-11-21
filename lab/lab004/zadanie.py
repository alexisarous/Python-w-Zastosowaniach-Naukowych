from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from rich.console import Console
import argparse

console = Console()
console.clear()

parser = argparse.ArgumentParser(description="Opis")
parser.add_argument('file', help='name of file')
args = parser.parse_args()


service = Service('chromedriver.exe')
driver = webdriver.Chrome(service = service)

#driver.maximize_window()

driver.get('https://radioaktywne.pl')

driver.find_element_by_id('jp-live-play').click() # włącza muzykę
driver.find_element_by_id('nav-tab-2').click() # zakładka nagrania

title = args.file + ".json"
x = []

for i in range(6):
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.execute_script("window.scrollBy(0,600)","")
    time.sleep(1)


divs = driver.find_elements(By.CLASS_NAME, 'nagranie-title')
for div in divs:
    #print(f"{div.text}")
    x.append(json.dumps(f"{div.text}", ensure_ascii=False))


with open(title, 'w') as f:
    json.dump(x, f)


driver.find_element_by_id('nav-tab-1').click() # powrót do głównej zakładki na 2s i zminimalizowanie okienka
time.sleep(2)
driver.minimize_window()


with open(title, 'r') as f:
    y = json.load(f)
    console.print(y)



# driver.close()