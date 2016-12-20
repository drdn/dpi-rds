#METADATA SCRAPER - Internet Archive
#Digital Collections @ University of Maryland, College Park
#David Durden (durden@umd.edu)

import sys, urllib, json, csvkit
from datetime import datetime
	
format = '%Y%m%d%H%M'
name = 'scrape_results'
path ='.csv'
new_file = '%s-%s%s' % (name, datetime.now().strftime(format), path)

start = '%s %s' % ('Started @', datetime.now())
print start

input_file = sys.argv[1]
with open(input_file, "r") as f1:
	ids = [i.strip("\n") for i in f1.readlines()]

	with open(new_file, 'w') as csvfile: 
		fieldnames = ['Identifier', 'Upload Date', 'Total Views', 'Title', 'Topic', 'Collection']
		writer = csvkit.py2.CSVKitDictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		
		for id in ids:
			record = {}
			dl1 = {}
			topic = {}
			url = "http://archive.org/details/{0}&output=json".format(id) 
			data = urllib.urlopen(url)	
			j1 = data.read()
			try:	
				jdata = json.loads(j1)
				if 'item' in jdata:
					record = {'Identifier': " ".join(jdata['metadata']['identifier']), 
						'Upload Date': " ".join(jdata['metadata']['addeddate']),
						'Total Views': jdata['item']['downloads'],
						'Title': " ".join(jdata['metadata']['title']),
						'Topic': " ".join(jdata['metadata']['subject']),
						'Collection': "; ".join(jdata['metadata']['collection'])}
					writer.writerow(record)
				else:
					record2 = {'Identifier': " ".join(jdata['metadata']['identifier']), 
						'Upload Date': " ".join(jdata['metadata']['addeddate']),
						'Total Views': '0',
						'Title': " ".join(jdata['metadata']['title']),
						'Topic': " ".join(jdata['metadata']['subject']),
						'Collection': "; ".join(jdata['metadata']['collection'])}
					writer.writerow(record2)	
			except:
				broken_record = {'Identifier': " ".join(jdata['metadata']['identifier']),
								'Upload Date': " ".join(jdata['metadata']['addeddate']),
								'Total Views': jdata['item']['downloads'],
								'Title': " ".join(jdata['metadata']['title']), 
								'Topic': "0 -- subject is missing",
								'Collection': "; ".join(jdata['metadata']['collection'])}
				writer.writerow(broken_record)
							
done = '%s %s' % ('Done @', datetime.now())
print done 	