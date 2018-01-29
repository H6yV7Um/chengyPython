import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawler_bible import crawler_auto

base_url = "https://www.wordproject.org/bibles/audio/12_japanese/index.htm"
pre_url = 'https://www.wordproject.org/bibles/audio/12_japanese/'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

with open("data/new_bible.txt", 'r') as openfile:
    for line in openfile.readlines():
        infos = line.split("\t")
        try:
            path = infos[0] + os.path.sep + infos[1] + os.path.sep
            url = pre_url + infos[2]
            browser.get(url)
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            zip_url = soup.select('.textOptions')[0].select('.ym-button')[0]['href']
            crawler_auto.getAudio(path, infos[1] + ".zip", zip_url, False)
            print("download " + infos[1] + " success")
        except Exception:
            print("download " + infos[1] + " failed")

# browser.get(base_url)
# time.sleep(3)
# html = browser.page_source
# soup = BeautifulSoup(html)
# book_dict = {}
# h3 = soup.select("#main > div > div > div > div.ym-grid.linearize-level-2 > div.ym-g50.ym-gl > h3")[0]
# key1, b, c = h3.stripped_strings
# book_dict1 = {}
# li_list = soup.select('#main > div > div > div > div.ym-grid.linearize-level-2 > div.ym-g50.ym-gl > ul')[0].select('li')
# for li in li_list:
#     a = li.select('a')[0]
#     value = a.text.strip()
#     book_dict1[value] = a['href']
# book_dict[key1] = book_dict1
# h3 = soup.select('#main > div > div > div > div.ym-grid.linearize-level-2 > div.ym-g50.ym-gr > h3')[0]
# key2, b = h3.stripped_strings
# book_dict2 = {}
# li_list = soup.select('#main > div > div > div > div.ym-grid.linearize-level-2 > div.ym-g50.ym-gr > ul')[0].select('li')
# for li in li_list:
#     a = li.select('a')[0]
#     value = a.text.strip()
#     book_dict2[value] = a['href']
# book_dict[key2] = book_dict2
#
# with open("data/new_bible.txt", 'w') as openfile:
#     for k, v in book_dict.items():
#         for chapter, url in v.items():
#             openfile.write(k + "\t" + chapter + "\t" + url + "\n")
