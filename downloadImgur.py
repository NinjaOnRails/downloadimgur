#! /usr/bin/env python3
# downloadImgur.py - Downloades all searched images from Imgur.
import sys
import requests, os, bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#searchCat = 'dolomites'
searchCat = '+'.join(sys.argv[1:])
url = 'http://imgur.com/search/score?q=%s' % searchCat
os.makedirs(sys.argv[1], exist_ok=True)
delay = 5

def imgDownloader(searchCat):
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    end = None
    while not end:
        try:
            end = browser.find_element_by_link_text('Discover more images.')
        except NoSuchElementException:
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #htmlElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, "html"))).send_keys(Keys.END)
    imgElem = WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    #imgElem = browser.find_elements_by_tag_name('img')
    print('Found: %s images.' % len(imgElem))
    if imgElem == []:
        print('Could not find any images.')
    else:
        for i in range(len(imgElem)):
            imgUrl = imgElem[i].get_attribute('src')
            print('Downloading image %s...' % imgUrl)
            res = requests.get(imgUrl)
            res.raise_for_status()
            imageFile = open(os.path.join(sys.argv[1], os.path.basename(imgUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()   

    print('Images downloaded: %s.' % len(imgElem))

imgDownloader(searchCat)
