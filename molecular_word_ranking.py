#execute from the command line
'''
$ pip install scrapy
$ pip install seCrawler
$ scrapy crawl keywordSpider -a keyword=stem\ cell\ metabolites -a se=bing -a pages=50
'''

#something about http://www.sciencedirect.com/science/article/pii/S016372589900073X broke bs4
#todo: only accept 200 status codes

from bs4 import BeautifulSoup
from collections import Counter
import urllib.request

def read_url_list_from_file(filename):
    with open(filename) as f:
        list = f.readlines()
        return [line.strip() for line in list]

def get_words(url):
    chars_to_remove = ['\n', '"', '.', '“', ':', ',', '<', '>', '[', ';', ']', '!', '(', ')', '\\', '_', '=', '”', '/']
    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'utf-8')
    soup = BeautifulSoup(urllib.request.urlopen(req), 'html.parser')
    text = soup.get_text(' ', strip=True).lower().replace('’', "'")
    text1 = ''.join([c if c not in chars_to_remove else ' ' for c in text])
    return text1.split(' ')
    #todo add rest of punctuation

def read_list_from_file(filename):
    with open(filename) as f:
        return set(([word.strip('\n') for word in f.readlines()]))

bad_words = ['ncbi', 'sciencedirect']

with open('urls.txt') as oldfile, open('editedurls.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)

links = read_url_list_from_file('urls_short.txt')
english = read_list_from_file('words.txt')

for link in links:
    all_words_combined = []
    try:
        word_list = get_words(link)
    except 'urllib.error.HTTPError: HTTP Error 403: Forbidden':
        print('error')

    final_word_list = [word for word in word_list if word not in english]
    all_words_combined.append(final_word_list)

single_list = [x for y in all_words_combined for x in y]
ranked_words = Counter(single_list).most_common
print(ranked_words)