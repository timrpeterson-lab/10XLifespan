import requests
import csv
import time

with open('20160109RJ755 HML Compounds available.csv','r') as csvinput:
	with open('20160109RJ755 HML Compounds available_v2.csv', 'w') as csvoutput:
		writer = csv.writer(csvoutput, lineterminator='\n')
		reader = csv.reader(csvinput)

		all = []
		row = next(reader)
		row.append('CID')
		all.append(row)

		for row in reader:
			#print row[1]
			response = requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/' + row[1] + '/cids/TXT')
			#print response.text
			#quit()
			row.append(response.text.strip())

			#row.append(row[0])
			all.append(row)

			#time.sleep(0.1)

		writer.writerows(all)







