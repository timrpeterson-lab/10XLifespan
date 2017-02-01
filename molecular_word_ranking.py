

#execute from the command line
'''
$ pip install scrapy
$ pip install seCrawler
$ scrapy crawl keywordSpider -a keyword=stem\ cell\ metabolites -a se=bing -a pages=50
'''

# The following is pseudo code
links = open('urls.txt')

content = ''
for link in links:
	if 'ncbi' in link: continue
	response = request(link)
	content = content + response

word_array = content.split()

word_dict = []
for word in word_array:
	if(word_dict[word] == 0) word_dict[word] = 0
	else word_dict[word]++

# http://stackoverflow.com/questions/3420122/filter-dict-to-contain-only-certain-keys
sort(word_dict, desc)



