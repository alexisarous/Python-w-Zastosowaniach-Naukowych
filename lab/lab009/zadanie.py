import multiprocessing as mp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from PIL import Image


def download(n):
    name = "img" + str(n) + ".png"

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = service)
    driver.get('http://if.pw.edu.pl/~mrow/dyd/wdprir')

    driver.find_element_by_link_text(name).click()

    with open(name, 'wb') as file:
        file.write(driver.find_element_by_xpath('/html/body/img').screenshot_as_png)

    
    img = Image.open(name)
    imgGray = img.convert('L')
    imgGray.save(name)
    
    driver.close()


if __name__ == '__main__':
    for i in range(10):
        p = mp.Process(target = download, args = (i,))
        p.start()


