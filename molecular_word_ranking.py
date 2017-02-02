

#execute from the command line
'''
$ pip install scrapy
$ pip install seCrawler
$ scrapy crawl keywordSpider -a keyword=stem\ cell\ metabolites -a se=bing -a pages=50
'''

#something about http://www.sciencedirect.com/science/article/pii/S016372589900073X broke bs4

from bs4 import BeautifulSoup
from collections import OrderedDict
import sys
import urllib.request


def get_words(url):
    chars_to_remove = ['\n', '"', '.', '“', ':', ',', '<', '>', '[', ']', '!', '(', ')', '\\', '_', '=', '”', '/']
    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'utf-8')
    # 200 is the HTTP success code.  For this type of request, any other code returned means the request failed
    #if req.status_code != 200:
    #    return None
    soup = BeautifulSoup(urllib.request.urlopen(req), 'html.parser')
    text = soup.get_text(' ', strip=True).lower().replace('’', "'")
    text1 = ''.join([c if c not in chars_to_remove else ' ' for c in text])
    return set(text1.split(' '))
    #todo add rest of punctuation

def read_list_from_file(filename):
    with open(filename) as f:
        return set(([word.strip('\n') for word in f.readlines()]))

english = read_list_from_file('words.txt')

source = get_words('http://www.pnas.org/content/78/12/7634.short')
filtered = source - english
print(filtered)

sys.exit()

with open('urls.txt') as f:
    links = f.readlines()

for link in links:
    if 'ncbi' in link:
        continue
    response = requests(link)
    content = content + response.text




