import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

proxies = {
    "http": "http://127.0.0.1:51263",
    "https": "http://127.0.0.1:51263",
}

pre_url = 'http://rekion.dl.ndl.go.jp'


def get_headless_chrome():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser


def get_audio_url_from_page(page_url):
    browser = get_headless_chrome()
    try:
        browser.get(page_url)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source)
        m3u8_url = soup.select('#source')[0]['src']
        return pre_url + m3u8_url
    finally:
        browser.quit()


def download_file(path, name, url, use_proxy=False):
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


def download_m3ufile(url):
    download_file("data/", "test.m3u", url, False)


def m3u_to_mp3(m3u_file_path, mp3_file_path):
    cmd = 'ffmpeg -protocol_whitelist file,tcp,http,crypto -i ' + m3u_file_path + ' -c copy ' + mp3_file_path
    res = os.popen(cmd).readlines()
    print(res)
