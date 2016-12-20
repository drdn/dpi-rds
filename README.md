id-generator.py is written in python 3 and requires the internetarchive module. This script uses a single search term to return a list of associated object identifiers. 

$ python3 id-generator.py {foo} bar.txt

md-scraper.py is written in python 2.7 and requires the json and csvkit modules. This script takes a .txt of object identifiers and returns a .csv that includes the following metadata fields: identifier, addeddate, downloads, title, subject, and collection.

$ python md-scraper.py bar.txt
