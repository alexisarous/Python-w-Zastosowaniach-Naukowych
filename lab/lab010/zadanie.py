from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image

import asyncio


async def download(n):
    name = "img" + str(n) + ".png"

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = service)
    driver.get('http://if.pw.edu.pl/~mrow/dyd/wdprir')

    await driver.find_element_by_link_text(name).click()

    with await open(name, 'wb') as file:
        file.write(driver.find_element_by_xpath('/html/body/img').screenshot_as_png)

    img = Image.open(name)
    imgGray = img.convert('L')
    imgGray.save(name)
    
    driver.close()

async def main():
    await asyncio.gather(*[download(n) for n in range(4)])


asyncio.run(main())