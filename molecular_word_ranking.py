# execute from the command line
"""
$ pip install scrapy
$ pip install seCrawler
$ scrapy crawl keywordSpider -a keyword=stem\ cell\ metabolism -a se=bing -a pages=50
"""

# something about http://www.sciencedirect.com/science/article/pii/S016372589900073X broke bs4

from bs4 import BeautifulSoup
import os
from subprocess import run
from collections import Counter
import urllib.request
import urllib.error
import time
import socket


def read_url_list_from_file(filename):
    with open(filename) as f:
        filelist = f.readlines()
        return [curline.strip('\n') for curline in filelist]


def strip_unwanted_characters_and_split(text):
    chars_to_remove = ['\n', '"', '.', '"', ':', '<', '>', '[', ';', ']', '!', '\\', '_', '=', '"', '/']
    text1 = ''.join([c if c not in chars_to_remove else ' ' for c in text])
    return [c for c in text1.split(' ') if c != '']


def get_words_from_pdf(url):
    file_name, headers = urllib.request.urlretrieve(url)
    run(['pdftotext.exe', file_name, 'tmp.txt'])
    os.remove(file_name)
    try:
        with open('tmp.txt', 'r') as f:
            wordsfromurl = strip_unwanted_characters_and_split(f.read())
        os.remove('tmp.txt')
    except FileNotFoundError:
        return []
    return wordsfromurl


def get_words(url):
    if url.endswith('.pdf'):
        return get_words_from_pdf(url)
    try:
        page_data = urllib.request.urlopen(url, timeout=10)
    except socket.timeout:
        return []
    if page_data.code != 200:
        return []
    soup = BeautifulSoup(page_data, 'html.parser')
    text = soup.get_text(' ', strip=True).lower().replace('’', "'")
    return strip_unwanted_characters_and_split(text)


def read_list_from_file(filename):
    with open(filename) as f:
        return set(([word.strip('\n') for word in f.readlines()]))

inter_request_interval_in_seconds = 5
bad_words = ['ncbi', 'sciencedirect', 'eypsb.us']
urls = read_url_list_from_file('urls2.txt')
pdf_urls = [url for url in urls if url.endswith('.pdf')]
bad_words_removed = [url for url in urls if not any(bad_word in url for bad_word in bad_words)]
print(len(urls))
print(len(pdf_urls))
print(len(bad_words_removed))

english = read_list_from_file('3000words.txt')
all_words_combined = []
next_request_time = time.time()

for link in bad_words_removed:
    while time.time() < next_request_time:
        print('Being nice...')
        time.sleep(next_request_time - time.time())
    try:
        print('Processing {0}'.format(link))
        words = get_words(link)
        next_request_time = time.time() + inter_request_interval_in_seconds
    except urllib.error.HTTPError as err:
        print('{0} on {1}'.format(type(err), link))
    except urllib.error.URLError as err:
        print('{0} on {1}'.format(type(err), link))
    except ValueError as err:
        print('{0} on {1}'.format(type(err), link))

    final_word_list = [word for word in words if word not in english]
    for word in final_word_list:
        all_words_combined.append(word)

ranked_words = Counter(all_words_combined).most_common
print(ranked_words)
