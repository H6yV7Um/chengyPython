import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

proxies = {
    "http": "http://127.0.0.1:51263",
    "https": "http://127.0.0.1:51263",
}

pre_url = 'https://www.jw.org'


def get_cn_book(url):
    browser = webdriver.Chrome()
    browser.get(url)




def get_books(url, html=None):
    book_info = {}
    if html is None:
        html = requests.get(url, proxies=proxies).text
    soup = BeautifulSoup(html)
    book_eles = soup.select("#onlineBibleTOCView > div > div.hebrewScriptures.clearfix")
    category = book_eles[0].select('h3')[0].text
    book_dict = {}
    book_list = book_eles[0].select('a')
    for book in book_list:
        key = book.select('.fullName')[0].text
        value = pre_url + book['href']
        book_dict[key] = value
    book_info[category] = book_dict
    book_eles = soup.select("#onlineBibleTOCView > div > div.greekScriptures.clearfix")
    category = book_eles[0].select('h3')[0].text
    book_dict = {}
    book_list = book_eles[0].select('a')
    for book in book_list:
        key = book.select('.fullName')[0].text
        value = pre_url + book['href']
        book_dict[key] = value
    book_info[category] = book_dict
    return book_info


def get_audio_info(url):
    html = requests.get(url, proxies=proxies).text
    soup = BeautifulSoup(html)
    a_list = soup.select('.chapters')[0].select('a')
    detail_list = []
    for a in a_list:
        detail_list.append(a['href'])
    browser = webdriver.Chrome()
    chapter_info = {}
    for chapter_url in detail_list:
        browser.get(pre_url + chapter_url)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        title = soup.select('#article > article > header > h1')[0].text
        title = title.strip('\n').strip('  ').strip('\n').strip('  ')
        title = title.replace(u'\xa0', u' ')
        audio_url = soup.select('audio')[0]['src']
        chapter_info[title] = audio_url
    browser.quit()
    return chapter_info


def getAudio(path, name, url, use_proxy=False):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path + name):
        if use_proxy:
            r = requests.get(url, proxies=proxies)
        else:
            r = requests.get(url)
        with open(path + name, 'wb') as code:
            code.write(r.content)
        r.close()


def download_bible(path, use_proxy=False):
    with open(path) as info_file:
        for row in info_file.readlines():
            info_list = row.strip('\n').split('\t')
            audio_path = "data" + os.path.sep + info_list[0] + os.path.sep + info_list[1] + os.path.sep
            file_name = info_list[2] + '.mp3'
            try:
                getAudio(audio_path, file_name, info_list[3], use_proxy=use_proxy)
            except Exception:
                if os.path.exists(audio_path + file_name):
                    os.remove(audio_path + file_name)
                print(audio_path + " failed")
