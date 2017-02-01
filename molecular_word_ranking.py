

#execute from the command line
'''
$ pip install scrapy
$ pip install seCrawler
$ scrapy crawl keywordSpider -a keyword=stem\ cell\ metabolites -a se=bing -a pages=50
'''

# The following is pseudo code

with open('urls.txt') as f:
    links = f.readlines()


content = ''
for link in links:
	if 'ncbi' in link: 
		continue
	response = requests(link)
	content = content + response.text

word_array = content.split()

word_dict = {}
for word in word_array:
	if(word_dict[word] == 0) word_dict[word] = 0
	else word_dict[word]++

# http://stackoverflow.com/questions/3420122/filter-dict-to-contain-only-certain-keys
sort(word_dict, desc)



